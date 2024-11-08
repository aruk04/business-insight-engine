import streamlit as st  # type: ignore
import mysql.connector  # type: ignore
import pandas as pd  # type: ignore
from create import create
from database import create_table, fetch_recommendations
from delete import delete
from read import read
from update import update

# Database connection
mydb = mysql.connector.connect(
    host="localhost",
    database="sbie",
    user="root",
    password="arushisql@p35"
)

def get_first_two_letters(b_id):
    """
    Extracts the first two letters of the business ID,
    ignoring any underscore and numbers.
    """
    return ''.join([char for char in b_id[:2] if char.isalpha()])

def main():
    st.title("SMART BUSINESS INSIGHT ENGINE")
    menu = ["Add", "View", "Edit", "Remove", "Give Recommendations"]
    choice = st.sidebar.selectbox("Menu", menu)

    create_table()  # Ensure tables are created if they don't exist

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

    elif choice == "Give Recommendations":
        st.subheader("Business Recommendations")
        business_id = st.text_input("Enter Business ID for Recommendations:")
        
        if st.button("Fetch Recommendations"):
            if business_id:
                # Extract the first two letters for recommendation filtering
                first_two_letters = get_first_two_letters(b_id)
                recommendations = fetch_recommendations(first_two_letters)
                
                if recommendations:
                    # Display each entity's records in separate tables
                    for table, records in recommendations.items():
                        if records:
                            st.write(f"**{table}**")
                            
                            # Convert records to DataFrame with column names based on the table
                            if table == "Competitors":
                                df = pd.DataFrame(records, columns=["C_Name"])
                            elif table == "Analysts":
                                df = pd.DataFrame(records, columns=["A_Name"])
                            elif table == "Investors":
                                df = pd.DataFrame(records, columns=["I_Name"])
                            elif table == "Partnership":
                                df = pd.DataFrame(records, columns=["P_Name"])
                            elif table == "Contracts":
                                df = pd.DataFrame(records, columns=["Con_ID", "Con_Type", "Validity Period", "I_ID"])
                            elif table == "Legal_Advisory":
                                df = pd.DataFrame(records, columns=["L_ID", "Adv_Name", "L_Experience", "Jurisdiction"])
                            elif table == "Vendor_Supplier":
                                df = pd.DataFrame(records, columns=["V_ID", "V_Name", "V_Type", "Budget", "Quality", "V_Loc"])
                            elif table == "Location":
                                df = pd.DataFrame(records, columns=["Loc_ID", "L_Name", "Market_Potential", "Region"])
                            elif table == "Beneficiary":
                                df = pd.DataFrame(records, columns=["Ben_ID", "Ben_Name", "Age", "DOB", "Lease_Term", "Mail", "Phone", "Owner"])
                            
                            # Display the DataFrame in Streamlit as a table
                            st.dataframe(df)  # Or use st.table(df) for a static table
                        else:
                            st.write(f"**{table}**")
                            st.write("No records found.")
                else:
                    st.write("No recommendations found for this Business ID.")
            else:
                st.write("Please enter a Business ID.")

if __name__ == '__main__':
    main()
