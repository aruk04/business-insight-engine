import streamlit as st
import mysql.connector


from create import create
from database import create_table
from delete import delete
from read import read
from update import update

import mysql.connector
mydb = mysql.connector.connect(
host="localhost",
database="sbie",
user="root",
password="arushisql@p35"
)


# Create a cursor to interact with the database
c = mydb.cursor()

# Sample query to read data from a table (replace 'your_table' with the actual table name)
c.execute("SELECT * FROM business")

# Fetch and print all rows from the table
rows = c.fetchall()
for row in rows:
    print(row)

# Close the cursor and connection
c.close()
mydb.close()


def main():
    st.title("SMART BUSINESS INSIGHT ENGINE")
    menu = ["Add", "View", "Edit", "Remove"]
    choice = st.sidebar.selectbox("Menu", menu)

    create_table()
    if choice == "Add":
        st.subheader("Enter Business Details:")
        create()

    elif choice == "View":
        st.subheader("View created details")
        read()

    elif choice == "Edit":
        st.subheader("Update created details")
        update()

    elif choice == "Remove":
        st.subheader("Delete created details")
        delete()

    else:
        st.subheader("About tasks")


if __name__ == '__main__':
    main()
