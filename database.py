# pip install mysql-connector-python
import mysql.connector #type: ignore

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="arushisql@p35",
    database="sbie"
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
                    );''')
    
    c.execute(''' CREATE TABLE IF NOT EXISTS Trends(
                    T_Type VARCHAR(50),
                    Duration INT,
                    Impact_level VARCHAR(50),
                    A_ID VARCHAR(50),
                    FOREIGN KEY (A_ID) REFERENCES ANALYSTS(A_ID)
                   );''')

    c.execute('''CREATE TABLE IF NOT EXISTS Contracts (
                    Con_ID VARCHAR(50) PRIMARY KEY,
                    Con_Type VARCHAR(50),
                    Validity_period INT,
                    B_ID VARCHAR(50),
                    I_ID VARCHAR(50),
                    FOREIGN KEY (B_ID) REFERENCES BUSINESS(B_ID),
                    FOREIGN KEY (I_ID) REFERENCES INVESTORS(I_ID)
                   );''')

    c.execute('''CREATE TABLE IF NOT EXISTS Legal_Advisory (
                    L_ID VARCHAR(50) PRIMARY KEY,
                    Adv_Name VARCHAR(100),
                    L_Experience INT,
                    Jurisdiction VARCHAR(100),
                    Con_ID VARCHAR(50),
                    FOREIGN KEY (Con_ID) REFERENCES CONTRACTS(Con_ID)
                   );''')

    c.execute('''CREATE TABLE IF NOT EXISTS Partnership (
                    P_ID VARCHAR(50) PRIMARY KEY,
                    P_Name VARCHAR(100),
                    P_Type VARCHAR(50),
                    P_Industry VARCHAR(50),
                    B_ID VARCHAR(50),
                    FOREIGN KEY (B_ID) REFERENCES BUSINESS(B_ID)
                   );''')

    c.execute('''CREATE TABLE IF NOT EXISTS Vendor_Supplier (
                    V_ID VARCHAR(50) PRIMARY KEY,
                    V_Name VARCHAR(100),
                    V_Type VARCHAR(50),
                    Budget DECIMAL(15, 2),
                    Quality VARCHAR(50),
                    V_loc VARCHAR(100),
                    B_ID VARCHAR(50),
                    FOREIGN KEY (B_ID) REFERENCES BUSINESS(B_ID)
                   );''')

    c.execute('''CREATE TABLE IF NOT EXISTS Location (
                    LOC_ID VARCHAR(50) PRIMARY KEY,
                    L_Name VARCHAR(100),
                    Market_potential VARCHAR(50),
                    Region VARCHAR(100),
                    V_ID VARCHAR(50),
                    FOREIGN KEY (V_ID) REFERENCES VENDOR_SUPPLIER(V_ID)
                   );''')

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
                   );''')

# Function to add a new business record
def add_data(b_id, b_name, l_name, f_name, b_type, oo_mail, phone):
    c.execute('''
        INSERT INTO BUSINESS (B_ID, B_Name, L_Name, F_Name, B_Type, OO_Mail, Phone) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (b_id, b_name, l_name, f_name, b_type, oo_mail, phone))
    mydb.commit()

# Function to retrieve all data from the Business table
def view_all_data():
    c.execute('SELECT * FROM BUSINESS')
    data = c.fetchall()
    return data

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
        SET B_ID = %s, B_Name = %s, L_Name = %s, F_Name = %s, B_Type = %s, OO_Mail = %s, Phone = %s 
        WHERE B_ID = %s AND B_Name = %s AND L_Name = %s AND F_Name = %s AND B_Type = %s AND OO_Mail = %s AND Phone = %s
    ''', (new_b_id, new_b_name, new_l_name, new_f_name, new_b_type, new_oo_mail, new_phone,
          b_id, b_name, l_name, f_name, b_type, oo_mail, phone))
    mydb.commit()

# Function to delete a business record by name
def delete_data(b_name):
    c.execute('DELETE FROM BUSINESS WHERE B_Name = %s', (b_name,))
    mydb.commit()



def fetch_recommendations(cursor, b_id):
    first_two_letters = b_id[:2]  # Extract the first two characters
    recommendations = {}

    # Competitors - Businesses with matching first two letters
    query = "SELECT B_Name FROM BUSINESS WHERE LEFT(B_ID, 2) = %s"
    cursor.execute(query, (first_two_letters,))
    recommendations["Competitors"] = cursor.fetchall()

    # Analysts
    query = "SELECT A_Name FROM ANALYSTS WHERE LEFT(B_ID, 2) = %s"
    cursor.execute(query, (first_two_letters,))
    recommendations["Analysts"] = cursor.fetchall()

    # Investors
    query = "SELECT I_Name FROM INVESTORS WHERE LEFT(B_ID, 2) = %s"
    cursor.execute(query, (first_two_letters,))
    recommendations["Investors"] = cursor.fetchall()

    # Partnerships
    query = "SELECT P_Name FROM PARTNERSHIP WHERE LEFT(B_ID, 2) = %s"
    cursor.execute(query, (first_two_letters,))
    recommendations["Partnership"] = cursor.fetchall()

    # Contracts
    query = "SELECT Con_ID, Con_Type, Validity_Period, I_ID FROM CONTRACTS WHERE LEFT(B_ID, 2) = %s"
    cursor.execute(query, (first_two_letters,))
    recommendations["Contracts"] = cursor.fetchall()

    # Legal Advisory
    query = "SELECT L_ID, Adv_Name, L_Experience, Jurisdiction FROM LEGAL_ADVISORY WHERE LEFT(B_ID, 2) = %s"
    cursor.execute(query, (first_two_letters,))
    recommendations["Legal_Advisory"] = cursor.fetchall()

    # Vendor Suppliers
    query = "SELECT V_ID, V_Name, V_Type, Budget, Quality, V_Loc FROM VENDOR_SUPPLIER WHERE LEFT(B_ID, 2) = %s"
    cursor.execute(query, (first_two_letters,))
    recommendations["Vendor_Suppliers"] = cursor.fetchall()

    # Beneficiaries
    query = "SELECT Ben_ID, Ben_Name, Age, DOB, Lease_Term, Mail, Phone, Owner FROM BENEFICIARY WHERE LEFT(B_ID, 2) = %s"
    cursor.execute(query, (first_two_letters,))
    recommendations["Beneficiaries"] = cursor.fetchall()

    return recommendations

