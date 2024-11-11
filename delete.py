import pandas as pd #type: ignore
import streamlit as st #type: ignore
from database import view_all_data, view_only_business_names, delete_data

def delete():
    # Fetch all data from the Business table
    result = view_all_data()
    df = pd.DataFrame(result, columns=['Business ID', 'Business Name', 'Legal Name', 'Founder Name', 'Business Type', 'Official Email', 'Phone Number'])
    
    with st.expander("Current Data"):
        st.dataframe(df)

    # List of business IDs for selection
    list_of_businesses = [i[0] for i in view_only_business_names()]
    selected_business = st.selectbox("Business to Delete", list_of_businesses)
    st.warning(f"Do you want to delete :: {selected_business}?")
    
    # Button to delete the selected business
    if st.button("Delete Business"):
        delete_data(selected_business)
        st.success(f"Business with ID {selected_business} has been deleted successfully")
    
    # Display updated data
    new_result = view_all_data()
    df2 = pd.DataFrame(new_result, columns=['Business ID', 'Business Name', 'Legal Name', 'Founder Name', 'Business Type', 'Official Email', 'Phone Number'])
    with st.expander("Updated Data"):
        st.dataframe(df2)