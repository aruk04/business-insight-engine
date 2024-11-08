import streamlit as st #type: ignore
import mysql.connector #type: ignore
import pandas as pd #type: ignore
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
                recommendations = fetch_recommendations(business_id)
                
                if recommendations:
                    # Display each entity's records in separate tables
                    for table, records in recommendations.items():
                        if records:
                            st.write(f"**{table}**")
                            
                            # Convert records to DataFrame with column names based on the table
                            if table == "Competitors":
                                df = pd.DataFrame(records, columns=["Competitor Name"])
                            elif table == "Analysts":
                                df = pd.DataFrame(records, columns=["Analyst Name"])
                            elif table == "Investors":
                                df = pd.DataFrame(records, columns=["Investor Name"])
                            elif table == "Partnerships":
                                df = pd.DataFrame(records, columns=["Partner Name"])
                            elif table == "Contracts":
                                df = pd.DataFrame(records, columns=["Contract ID", "Contract Type", "Validity Period", "Investor ID"])
                            elif table == "Legal_Advisory":
                                df = pd.DataFrame(records, columns=["Legal Advisor ID", "Advisor Name", "Experience", "Jurisdiction"])
                            elif table == "Vendor_Suppliers":
                                df = pd.DataFrame(records, columns=["Vendor ID", "Vendor Name", "Type", "Budget", "Quality", "Location"])
                            elif table == "Locations":
                                df = pd.DataFrame(records, columns=["Location ID", "Location Name", "Market Potential", "Region"])
                            elif table == "Beneficiaries":
                                df = pd.DataFrame(records, columns=["Beneficiary ID", "Name", "Age", "DOB", "Lease Term", "Email", "Phone", "Owner"])
                            
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
