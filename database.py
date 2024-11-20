import mysql.connector #type: ignore
import streamlit as st #type: ignore
import pandas as pd #type: ignore
from connection import get_connection

mydb = mysql.connector.connect(
        host="localhost",
        database="sbie",
        user="root",
        password="***********"
)
c = mydb.cursor()

# Function to create the Business table if it doesn't already exist
def create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS Business(
            B_ID VARCHAR(50) PRIMARY KEY,
            B_Name VARCHAR(100),
            L_Name VARCHAR(100),
            F_Name VARCHAR(100),
            B_Type VARCHAR(50),
            OO_Mail VARCHAR(100),
            Phone VARCHAR(15)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS Competitors (
            C_ID VARCHAR(50) PRIMARY KEY,
            C_Name VARCHAR(100),
            Industry_type VARCHAR(50),
            Prod_Sold INT,
            B_ID VARCHAR(50),
            FOREIGN KEY (B_ID) REFERENCES BUSINESS(B_ID)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS Analysts (
            A_ID VARCHAR(50) PRIMARY KEY,
            A_Name VARCHAR(100),
            Success_rate DECIMAL(5, 2),
            Experience INT,
            Salary DECIMAL(10, 2),
            B_ID VARCHAR(50),
            FOREIGN KEY (B_ID) REFERENCES BUSINESS(B_ID)
        )
    ''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS Investors (
                    I_ID VARCHAR(50) PRIMARY KEY,
                    I_Name VARCHAR(100),
                    Industry_pref VARCHAR(50),
                    Budget DECIMAL(15, 2),
                    B_ID VARCHAR(50),
                    FOREIGN KEY (B_ID) REFERENCES BUSINESS(B_ID)
        );
    ''')
    
    c.execute(''' CREATE TABLE IF NOT EXISTS Trends(
                    T_Type VARCHAR(50),
                    Duration INT,
                    Impact_level VARCHAR(50),
                    A_ID VARCHAR(50),
                    FOREIGN KEY (A_ID) REFERENCES ANALYSTS(A_ID)
        );
    ''')

    c.execute('''CREATE TABLE IF NOT EXISTS Contracts (
                    Con_ID VARCHAR(50) PRIMARY KEY,
                    Con_Type VARCHAR(50),
                    Validity_period INT,
                    B_ID VARCHAR(50),
                    I_ID VARCHAR(50),
                    FOREIGN KEY (B_ID) REFERENCES BUSINESS(B_ID),
                    FOREIGN KEY (I_ID) REFERENCES INVESTORS(I_ID)
        );
    ''')

    c.execute('''CREATE TABLE IF NOT EXISTS Legal_Advisory (
                    L_ID VARCHAR(50) PRIMARY KEY,
                    Adv_Name VARCHAR(100),
                    L_Experience INT,
                    Jurisdiction VARCHAR(100),
                    Con_ID VARCHAR(50),
                    FOREIGN KEY (Con_ID) REFERENCES CONTRACTS(Con_ID)
        );
    ''')

    c.execute('''CREATE TABLE IF NOT EXISTS Partnership (
                    P_ID VARCHAR(50) PRIMARY KEY,
                    P_Name VARCHAR(100),
                    P_Type VARCHAR(50),
                    P_Industry VARCHAR(50),
                    B_ID VARCHAR(50),
                    FOREIGN KEY (B_ID) REFERENCES BUSINESS(B_ID)
        );
    ''')

    c.execute('''CREATE TABLE IF NOT EXISTS Vendor_Supplier (
                    V_ID VARCHAR(50) PRIMARY KEY,
                    V_Name VARCHAR(100),
                    V_Type VARCHAR(50),
                    Budget DECIMAL(15, 2),
                    Quality VARCHAR(50),
                    V_loc VARCHAR(100),
                    B_ID VARCHAR(50),
                    FOREIGN KEY (B_ID) REFERENCES BUSINESS(B_ID)
                   
        );
    ''')

    c.execute('''CREATE TABLE IF NOT EXISTS Location (
                    LOC_ID VARCHAR(50) PRIMARY KEY,
                    L_Name VARCHAR(100),
                    Market_potential VARCHAR(50),
                    Region VARCHAR(100),
                    V_ID VARCHAR(50),
                    FOREIGN KEY (V_ID) REFERENCES VENDOR_SUPPLIER(V_ID)
        );
    ''')

    c.execute('''CREATE TABLE IF NOT EXISTS Beneficiary (
                    Ben_ID VARCHAR(50) PRIMARY KEY,
                    Ben_Name VARCHAR(100),
                    Age INT,
                    DOB DATE,
                    Lease_Term INT,
                    Mail VARCHAR(100),
                    Phone VARCHAR(15),
                    Owner VARCHAR(100),
                    B_ID VARCHAR(50),
                    FOREIGN KEY (B_ID) REFERENCES BUSINESS(B_ID)
        );
    ''')

# Function to add a new business record
def add_data(b_id, b_name, l_name, f_name, b_type, oo_mail, phone):
    c.execute('''
        INSERT INTO BUSINESS (B_ID, B_Name, L_Name, F_Name, B_Type, OO_Mail, Phone) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (b_id, b_name, l_name, f_name, b_type, oo_mail, phone))
    mydb.commit()

# Function to retrieve all data from the Business table
def view_all_data():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM BUSINESS")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result



# Function to view only business names (or IDs) for selection
def view_only_business_names():
    c.execute('SELECT B_Name FROM BUSINESS')
    data = c.fetchall()
    return data

# Function to retrieve details of a specific business by name
def get_business(b_name):
    c.execute('SELECT * FROM BUSINESS WHERE B_Name = %s', (b_name,))
    data = c.fetchall()
    return data

# Function to edit a business record
def edit_business_data(new_b_id, new_b_name, new_l_name, new_f_name, new_b_type, new_oo_mail, new_phone, 
                       b_id, b_name, l_name, f_name, b_type, oo_mail, phone):
    c.execute('''
        UPDATE BUSINESS 
        SET B_ID = %s, B_Name = %s, F_Name = %s, L_Name = %s, B_Type = %s, OO_Mail = %s, Phone = %s 
        WHERE B_ID = %s AND B_Name = %s AND L_Name = %s AND F_Name = %s AND B_Type = %s AND OO_Mail = %s AND Phone = %s
    ''', (new_b_id, new_b_name, new_l_name, new_f_name, new_b_type, new_oo_mail, new_phone,
          b_id, b_name, l_name, f_name, b_type, oo_mail, phone))
    mydb.commit()

# Function to delete a business record by name
def delete_data(b_name):
    c.execute('DELETE FROM BUSINESS WHERE B_Name = %s', (b_name,))
    mydb.commit()

def execute_procedure(cursor):
    """Executes the ArchiveShortDurationTrends stored procedure without parameters."""
    try:
        # Call the stored procedure without any parameters
        cursor.callproc('ArchiveShortDurationTrends')
        cursor.connection.commit()  # Commit the transaction
        return True
    except mysql.connector.Error as e:
        print(f"Database Error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False



def fetch_recommendations(cursor, B_ID):
    try:
        # Input validation
        if not B_ID or len(B_ID) < 2:
            return "Invalid Business ID. ID must be at least 2 characters long."

        first_two_letters = B_ID[:2]
        recommendations = {}

        # First verify if the business exists
        cursor.execute("SELECT B_ID FROM Business WHERE B_ID = %s", (B_ID,))
        if not cursor.fetchone():
            return "Business ID not found in database."

        try:
            # Fetch all recommendations with proper error handling
            queries = {
                "Competitors": """
                    SELECT C_ID, C_Name, Industry_Type, Prod_Sold, B_ID 
                    FROM Competitors 
                    WHERE LEFT(B_ID, 2) = %s
                """,
                "Analysts": """
                    SELECT A_ID, A_Name, Success_rate, Experience, Salary, B_ID 
                    FROM Analysts 
                    WHERE LEFT(B_ID, 2) = %s
                """,
                "Investors": """
                    SELECT I_ID, I_Name, Industry_pref, Budget, B_ID 
                    FROM Investors 
                    WHERE LEFT(B_ID, 2) = %s
                """,
                "Partnership": """
                    SELECT P_ID, P_Name, P_Type, P_Industry, B_ID 
                    FROM Partnership 
                    WHERE LEFT(B_ID, 2) = %s
                """,
                "Contracts": """
                    SELECT Con_ID, Con_Type, Validity_period, B_ID, I_ID 
                    FROM Contracts 
                    WHERE LEFT(B_ID, 2) = %s
                """,
                "Legal_Advisory": """
                    SELECT l.L_ID, l.Adv_Name, l.L_Experience, l.Jurisdiction
                    FROM Legal_Advisory l
                    JOIN Contracts c ON l.Con_ID = c.Con_ID
                    WHERE LEFT(c.B_ID, 2) = %s
                """,
                "Vendor_Supplier": """
                    SELECT V_ID, V_Name, V_Type, Budget, Quality, V_loc, B_ID 
                    FROM Vendor_Supplier 
                    WHERE LEFT(B_ID, 2) = %s
                """,
                "Location": """
                    SELECT l.LOC_ID, l.L_Name, l.Market_potential, l.Region, l.V_ID
                    FROM Location l
                    JOIN Vendor_Supplier v ON l.V_ID = v.V_ID
                    WHERE LEFT(v.B_ID, 2) = %s
                """,
                "Trends": """
                    SELECT t.T_Type, t.Duration, t.Impact_level, t.A_ID
                    FROM Trends t
                    JOIN Analysts a ON t.A_ID = a.A_ID
                    WHERE LEFT(a.B_ID, 2) = %s
                """,
                "Beneficiary": """
                    SELECT Ben_ID, Ben_Name, Age, DOB, Lease_Term, Mail, Phone, Owner, B_ID 
                    FROM Beneficiary 
                    WHERE LEFT(B_ID, 2) = %s
                """
            }

            for table_name, query in queries.items():
                try:
                    cursor.execute(query, (first_two_letters,))
                    results = cursor.fetchall()
                    recommendations[table_name] = results
                except mysql.connector.Error as table_err:
                    st.warning(f"Error fetching {table_name}: {table_err}")
                    recommendations[table_name] = []

            # Check if any data was found
            if all(len(records) == 0 for records in recommendations.values()):
                return f"No related data found for Business ID starting with '{first_two_letters}'"

            return recommendations

        except mysql.connector.Error as err:
            return f"Database error: {err}"

    except Exception as e:
        return f"Error: {str(e)}"
