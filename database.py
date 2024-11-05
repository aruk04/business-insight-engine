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
