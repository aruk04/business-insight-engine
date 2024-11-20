import pandas as pd #type: ignore
import streamlit as st #type: ignore
from database import view_all_data, view_only_business_names, delete_data
from connection import get_connection

def delete():
    # Fetch all data from the Business table
    result = view_all_data()
    df = pd.DataFrame(result, columns=['Business ID', 'Business Name', 'Last Name', 'First Name', 
                                     'Business Type', 'Official Email', 'Phone Number'])
    
    with st.expander("Current Data"):
        st.dataframe(df)

    # List of business IDs for selection
    list_of_businesses = [i[0] for i in view_only_business_names()]
    selected_business = st.selectbox("Business to Delete", list_of_businesses)
    st.warning(f"Do you want to delete :: {selected_business}?")
    
    # Button to delete the selected business
    if st.button("Delete Business"):
        connection = get_connection()
        cursor = connection.cursor()
        try:
            # Disable foreign key checks temporarily to avoid issues with foreign key constraints
            cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')

            # Delete from the BUSINESS table (trigger will handle related deletions)
            cursor.execute('DELETE FROM BUSINESS WHERE B_Name = %s', (selected_business,))

            # Commit the changes
            connection.commit()
            st.success(f"Business with name {selected_business} and all related data has been deleted successfully")

        except Exception as e:
            # Rollback in case of error
            connection.rollback()
            st.error(f"Error deleting business with name {selected_business}: {str(e)}")
        finally:
            # Re-enable foreign key checks
            cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
            cursor.close()
            connection.close()

    # Display updated data
    new_result = view_all_data()
    df2 = pd.DataFrame(new_result, columns=['Business ID', 'Business Name', 'Last Name', 'First Name', 
                                          'Business Type', 'Official Email', 'Phone Number'])
    with st.expander("Updated Data"):
        st.dataframe(df2)
