import streamlit as st #type: ignore
from mysql.connector import Error  #type: ignore
import mysql.connector #type: ignore
import pandas as pd #type: ignore
from create import create
from database import create_table, fetch_recommendations, execute_procedure
from delete import delete
from read import read
from update_business import update
from connection import get_connection
    

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'role' not in st.session_state:
    st.session_state.role = ''

def init_connection():
    return mysql.connector.connect(
        host="localhost",
        database="sbie",
        user="root",
        password="arushisql@p35"
    )

def verify_login(cursor, username, password, role):
    """Verify login credentials against database"""
    if role == 'admin':
        query = "SELECT * FROM admin WHERE admin_username = %s AND admin_password = %s"
    else:
        query = "SELECT * FROM agent WHERE agent_username = %s AND agent_password = %s"
    
    cursor.execute(query, (username, password))
    return cursor.fetchone() is not None

def register_user(cursor, mydb, username, password, role):
    """Register a new user in the database"""
    try:
        if role == 'admin':
            query = "INSERT INTO admin (admin_username, admin_password) VALUES (%s, %s)"
        else:
            query = "INSERT INTO agent (agent_username, agent_password) VALUES (%s, %s)"
        
        cursor.execute(query, (username, password))
        mydb.commit()
        return True, "Registration successful!"
    except mysql.connector.Error as err:
        if err.errno == 1062:  # Duplicate entry error
            return False, "Username already exists!"
        return False, f"Error: {str(err)}"

def login_page():
    st.title("SMART BUSINESS INSIGHT ENGINE")
    
    # Create tabs for login and registration
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    # Login Tab
    with tab1:
        st.subheader("Login")
        with st.form('login_form'):
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            role = st.selectbox('Role', ['admin', 'agent'])
            submit = st.form_submit_button('Login')
            
            if submit:
                try:
                    mydb = init_connection()
                    cursor = mydb.cursor()
                    
                    if verify_login(cursor, username, password, role):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.role = role
                        st.success('Login successful!')
                        st.experimental_rerun()
                    else:
                        st.error('Invalid credentials!')
                finally:
                    if 'cursor' in locals():
                        cursor.close()
                    if 'mydb' in locals():
                        mydb.close()
    
    # Registration Tab
    with tab2:
        st.subheader("Register New User")
        with st.form('registration_form'):
            new_username = st.text_input('New Username')
            new_password = st.text_input('New Password', type='password')
            confirm_password = st.text_input('Confirm Password', type='password')
            new_role = st.selectbox('Role', ['admin', 'agent'])
            register_submit = st.form_submit_button('Register')
            
            if register_submit:
                if new_password != confirm_password:
                    st.error("Passwords don't match!")
                elif len(new_password) < 8:
                    st.error("Password must be at least 8 characters long!")
                else:
                    try:
                        mydb = init_connection()
                        cursor = mydb.cursor()
                        
                        success, message = register_user(cursor, mydb, new_username, new_password, new_role)
                        if success:
                            st.success(message)
                            st.info("Please go to the Login tab to sign in.")
                        else:
                            st.error(message)
                    finally:
                        if 'cursor' in locals():
                            cursor.close()
                        if 'mydb' in locals():
                            mydb.close()

def archive_short_duration_trends():
    """Function to call the stored procedure to archive short duration trends and display archived data."""

    # Initialize session state variables
    if 'test_clicked' not in st.session_state:
        st.session_state.test_clicked = False
    if 'archive_clicked' not in st.session_state:
        st.session_state.archive_clicked = False
    if 'undo_clicked' not in st.session_state:
        st.session_state.undo_clicked = False
    if 'test_status' not in st.session_state:
        st.session_state.test_status = None
    if 'archive_status' not in st.session_state:
        st.session_state.archive_status = None
    if 'duration' not in st.session_state:
        st.session_state.duration = 1
    if 'archived_trends' not in st.session_state:
        st.session_state.archived_trends = None

    def handle_test_click():
        st.session_state.test_clicked = True

    def handle_archive_click():
        st.session_state.archive_clicked = True

    def handle_undo_click():
        st.session_state.undo_clicked = True

    def test_connection():
        try:
            mydb = init_connection()
            cursor = mydb.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            mydb.close()
            st.session_state.test_status = "success"
        except Exception as e:
            st.session_state.test_status = f"error: {str(e)}"

    def perform_archive(duration):
        try:
            mydb = init_connection()
            cursor = mydb.cursor(dictionary=True)
            
            # Check for eligible trends
            cursor.execute("SELECT COUNT(*) as count FROM trends WHERE Duration <= %s", (duration,))
            count = cursor.fetchone()['count']
            
            if count == 0:
                st.session_state.archive_status = "no_trends"
                cursor.close()
                mydb.close()
                return
                
            # Execute archive procedure
            cursor.callproc("ArchiveShortDurationTrends", [duration])
            mydb.commit()

            # Fetch archived trends to display
            cursor.execute("SELECT * FROM archivedtrends ORDER BY Duration ASC")
            st.session_state.archived_trends = cursor.fetchall()

            st.session_state.archive_status = "success"
            cursor.close()
            mydb.close()
        except Exception as e:
            st.session_state.archive_status = f"error: {str(e)}"

    #st.title("SMART BUSINESS INSIGHT ENGINE")
    #st.subheader("Archive Short Duration Trends")

    # Test connection button
    st.button("Test Connection", key="test_db_button", on_click=handle_test_click)

    if st.session_state.test_clicked:
        test_connection()
        if st.session_state.test_status == "success":
            st.success("Database connection successful!")
        elif st.session_state.test_status:
            st.error(f"Database connection failed: {st.session_state.test_status}")
        st.session_state.test_clicked = False

    # Duration input
    st.write("Enter Duration (in years) to Archive Trends")
    duration = st.number_input(
        "Duration (years):",
        min_value=1,
        value=st.session_state.duration,
        key="duration_input",
        on_change=lambda: setattr(st.session_state, 'duration', st.session_state.duration_input)
    )

    # Display current trends
    try:
        mydb = init_connection()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM trends ORDER BY Duration ASC")
        current_trends = cursor.fetchall()

        st.subheader("Current Trends")
        if current_trends:
            df = pd.DataFrame(current_trends)
            st.dataframe(df)
        else:
            st.info("No trends currently in the database.")
        cursor.close()
        mydb.close()
    except Exception as e:
        st.error(f"Error displaying trends: {str(e)}")

    # Archive and Undo buttons
    col1, col2 = st.columns(2)
    col1.button("Archive Now", key="archive_button", on_click=handle_archive_click)
    col2.button("Undo Archive", key="undo_button", on_click=handle_undo_click)

    # Handle archive operation
    if st.session_state.archive_clicked:
        perform_archive(duration)
        st.session_state.archive_clicked = False

    # Handle undo operation
    if st.session_state.undo_clicked:
        try:
            mydb = init_connection()
            cursor = mydb.cursor()
            cursor.callproc("UndoArchiveTrends")
            mydb.commit()
            st.session_state.archive_status = "undo_success"
            st.session_state.archived_trends = None  # Reset archived trends on undo
            cursor.close()
            mydb.close()
        except Exception as e:
            st.session_state.archive_status = f"undo_error: {str(e)}"
        st.session_state.undo_clicked = False

    # Display archive status
    if st.session_state.archive_status:
        if st.session_state.archive_status == "success":
            st.success("Successfully archived trends!")
        elif st.session_state.archive_status == "no_trends":
            st.warning("No trends found with the specified duration.")
        elif st.session_state.archive_status == "undo_success":
            st.success("Successfully undid archive!")
        elif "error" in st.session_state.archive_status:
            st.error(f"Error: {st.session_state.archive_status}")

        # Reset status for better experience
        st.session_state.archive_status = None

    # Display archived trends
    if st.session_state.archived_trends:
        st.subheader("Archived Trends")
        df_archived = pd.DataFrame(st.session_state.archived_trends)
        st.dataframe(df_archived)


             


    #except mysql.connector.Error as err:
    #    st.error(f"Database Error: {err}")
    #except Exception as e:
        #st.error(f"An error occurred: {e}")



def main():
    try:
        mydb = init_connection()
        c = mydb.cursor(buffered=True)

        # Check if user is logged in
        if not st.session_state.logged_in:
            login_page()
            return

        st.title("SMART BUSINESS INSIGHT ENGINE")
        
        # Display user info and logout in sidebar
        with st.sidebar:
            st.write(f"Logged in as: {st.session_state.username}")
            st.write(f"Role: {st.session_state.role}")
            if st.button('Logout'):
                st.session_state.logged_in = False
                st.session_state.username = ''
                st.session_state.role = ''
                # st.experimental_rerun()

        # Menu options based on role
        if st.session_state.role == 'admin':
            menu = ["Add", "View", "Edit", "Remove", "Give Recommendations", "Archived Trends"]
        else:  # agent role
            menu = ["Add", "View", "Give Recommendations"]
            
        choice = st.sidebar.selectbox("Menu", menu)

        create_table()  # Ensure tables are created if they don't exist

        if choice == "Add":
            st.subheader("Enter Business Details:")
            create()

        elif choice == "View":
            st.subheader("View created details")
            read(c)

        elif choice == "Edit" and st.session_state.role == 'admin':
            st.subheader("Update created details")
            update(c, mydb)

        elif choice == "Remove" and st.session_state.role == 'admin':
            st.subheader("Delete created details")
            delete()


        elif choice == "Archived Trends" and st.session_state.role == 'admin':
            st.subheader("Archive Short Duration Trends")
            if st.button("Archive Now"):
                archive_short_duration_trends()


        elif choice == "Give Recommendations":
            st.subheader("Business Recommendations")
            business_id = st.text_input("Enter Business ID for Recommendations:")
            
            if st.button("Fetch Recommendations"):
                if business_id:
                    with st.spinner("Fetching recommendations..."):
                        recommendations = fetch_recommendations(c, business_id)
                        
                        if isinstance(recommendations, str):
                            st.error(recommendations)
                        elif recommendations:
                            for table, records in recommendations.items():
                                if records:
                                    st.write(f"\n### {table} Records:")
                                    column_names = {
                                        "Competitors": ["C_ID", "C_Name", "Industry_Type", "Prod_Sold", "B_ID"],
                                        "Analysts": ["A_ID", "A_Name", "Success_rate", "Experience", "Salary", "B_ID"],
                                        "Investors": ["I_ID", "I_Name", "Industry_pref", "Budget", "B_ID"],
                                        "Partnership": ["P_ID", "P_Name", "P_Type", "P_Industry", "B_ID"],
                                        "Contracts": ["Con_ID", "Con_Type", "Validity_period", "B_ID", "I_ID"],
                                        "Legal_Advisory": ["L_ID", "Adv_Name", "L_Experience", "Jurisdiction"],
                                        "Vendor_Supplier": ["V_ID", "V_Name", "V_Type", "Budget", "Quality", "V_loc", "B_ID"],
                                        "Location": ["LOC_ID", "L_Name", "Market_potential", "Region", "V_ID"],
                                        "Trends": ["T_Type", "Duration", "Impact_level", "A_ID"],
                                        "Beneficiary": ["Ben_ID", "Ben_Name", "Age", "DOB", "Lease_Term", "Mail", "Phone", "Owner", "B_ID"]
                                    }
                                    
                                    if table in column_names:
                                        df = pd.DataFrame(records, columns=column_names[table])
                                        st.dataframe(df)
                                    else:
                                        st.error(f"Unknown table type: {table}")
                                else:
                                    st.info(f"No records found in {table}.")
                        else:
                            st.warning("No recommendations found for this Business ID.")
                else:
                    st.warning("Please enter a Business ID.")




    except mysql.connector.Error as err:
        st.error(f"Database Error: {err}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        if 'c' in locals():
            c.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

if __name__ == "__main__":
    main()
