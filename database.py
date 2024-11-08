# pip install mysql-connector-python
import mysql.connector

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
        CREATE TABLE IF NOT EXISTS BUSINESS(
            B_ID VARCHAR(50) PRIMARY KEY,
            B_Name VARCHAR(100),
            L_Name VARCHAR(100),
            F_Name VARCHAR(100),
            B_Type VARCHAR(50),
            OO_Mail VARCHAR(100),
            Phone VARCHAR(15)
        )
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


# Function to fetch recommendations based on the first two letters of the Business ID (B_ID)
def fetch_recommendations(first_two_letters):
    recommendations = {}

    # Competitors - Businesses with matching first two letters
    query = "SELECT B_Name FROM BUSINESS WHERE LEFT(B_ID, 2) = %s"
    c.execute(query, (first_two_letters,))
    recommendations["Competitors"] = c.fetchall()

    # Analysts - Fetch analysts based on the business ID pattern
    # Assuming `ANALYSTS` table has a `B_ID` foreign key or similar field
    query = "SELECT Analyst_Name FROM ANALYSTS WHERE LEFT(B_ID, 2) = %s"
    c.execute(query, (first_two_letters,))
    recommendations["Analysts"] = c.fetchall()

    # Investors - Fetch investors associated with businesses that match the first two letters
    # Assuming `INVESTORS` table has a `B_ID` or similar field
    query = "SELECT Investor_Name FROM INVESTORS WHERE LEFT(B_ID, 2) = %s"
    c.execute(query, (first_two_letters,))
    recommendations["Investors"] = c.fetchall()

    # Partnerships - Fetch partnerships based on the business ID pattern
    # Assuming `PARTNERSHIPS` table has a `B_ID` field
    query = "SELECT Partner_Name FROM PARTNERSHIPS WHERE LEFT(B_ID, 2) = %s"
    c.execute(query, (first_two_letters,))
    recommendations["Partnerships"] = c.fetchall()

    # Contracts - Fetch contracts linked with the business ID pattern
    # Assuming `CONTRACTS` table has relevant fields
    query = "SELECT Contract_ID, Contract_Type, Validity_Period, Investor_ID FROM CONTRACTS WHERE LEFT(B_ID, 2) = %s"
    c.execute(query, (first_two_letters,))
    recommendations["Contracts"] = c.fetchall()

    # Legal Advisory - Fetch legal advisors based on business ID pattern
    # Assuming `LEGAL_ADVISORY` table has a `B_ID` field
    query = "SELECT Legal_Advisor_ID, Advisor_Name, Experience, Jurisdiction FROM LEGAL_ADVISORY WHERE LEFT(B_ID, 2) = %s"
    c.execute(query, (first_two_letters,))
    recommendations["Legal_Advisory"] = c.fetchall()

    # Vendor Suppliers - Fetch vendors based on business ID pattern
    # Assuming `VENDOR_SUPPLIERS` table has a `B_ID` field
    query = "SELECT Vendor_ID, Vendor_Name, Type, Budget, Quality, Location FROM VENDOR_SUPPLIERS WHERE LEFT(B_ID, 2) = %s"
    c.execute(query, (first_two_letters,))
    recommendations["Vendor_Suppliers"] = c.fetchall()

    # Locations - Fetch locations associated with the business ID pattern
    # Assuming `LOCATIONS` table has a `B_ID` field
    query = "SELECT Location_ID, Location_Name, Market_Potential, Region FROM LOCATIONS WHERE LEFT(B_ID, 2) = %s"
    c.execute(query, (first_two_letters,))
    recommendations["Locations"] = c.fetchall()

    # Beneficiaries - Fetch beneficiaries based on the business ID pattern
    # Assuming `BENEFICIARIES` table has a `B_ID` field
    query = "SELECT Beneficiary_ID, Name, Age, DOB, Lease_Term, Email, Phone, Owner FROM BENEFICIARIES WHERE LEFT(B_ID, 2) = %s"
    c.execute(query, (first_two_letters,))
    recommendations["Beneficiaries"] = c.fetchall()

    return recommendations

