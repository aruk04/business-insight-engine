# connection.py
import mysql.connector #type: ignore

def get_connection():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            database="sbie",
            user="root",
            password="************"
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return None
