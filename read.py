import streamlit as st #type: ignore
import pandas as pd #type: ignore
import plotly.express as px #type: ignore
from database import view_all_data

def read(cursor):
    """
    Display business details and related information from the database.
    
    Args:
        cursor: MySQL database cursor object
    """
    # Fetch the data from the database
    result = view_all_data()
    
    # Dictionary mapping table names to their column names
    tables = {
        'Business': ['Business ID', 'Business Name', 'Last Name', 'First Name', 'Business Type', 'Official Email', 'Phone Number']
    }
    
    # Create a selectbox for table selection
    selected_table = st.selectbox("Select table to view:", list(tables.keys()))
    
    try:
        # Construct and execute query
        query = f"SELECT * FROM `{selected_table}`"
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            # Create DataFrame with appropriate column names
            df = pd.DataFrame(results, columns=tables[selected_table])
            st.dataframe(df)
        else:
            st.info(f"No records found in {selected_table} table.")
            
    except Exception as e:
        st.error(f"Error retrieving data: {str(e)}")
