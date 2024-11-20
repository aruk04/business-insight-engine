import pandas as pd #type: ignore
import streamlit as st #type: ignore
from database import view_all_data, view_only_business_names, get_business, edit_business_data

def update(c, mydb):
    # Fetch all data from the Business table
    result = view_all_data()
    df = pd.DataFrame(result, columns=['Business ID', 'Business Name', 'Last Name', 'First Name', 'Business Type', 'Official Email', 'Phone Number'])
    
    with st.expander("Current Businesses"):
        st.dataframe(df)
    
    # List of all business names for selection
    list_of_businesses = [i[0] for i in view_only_business_names()]
    selected_business = st.selectbox("Business to Edit", list_of_businesses)
    selected_result = get_business(selected_business)

    if selected_result:
        business_id = selected_result[0][0]
        business_name = selected_result[0][1]
        last_name = selected_result[0][2]
        first_name = selected_result[0][3]
        business_type = selected_result[0][4]
        official_email = selected_result[0][5]
        phone_number = selected_result[0][6]

        # Layout for editing business details
        col1, col2 = st.columns(2)
        with col1:
            new_business_id = st.text_input("Business ID:", business_id)
            new_business_name = st.text_input("Business Name:", business_name)
            new_last_name = st.text_input("Last Name:", last_name)
            new_first_name = st.text_input("First Name:", first_name)
        with col2:
            new_business_type = st.selectbox("Business Type:", ["Fashion", "Travel", "Sports", "Food"], index=["Fashion", "Travel", "Sports", "Food"].index(business_type))
            new_official_email = st.text_input("Official Email:", official_email)
            new_phone_number = st.text_input("Phone Number:", phone_number)
        
        # Button to update business details
        if st.button("Update Business"):
            edit_business_data(new_business_id, new_business_name,  new_last_name, new_first_name, new_business_type, new_official_email, new_phone_number, business_id, business_name, last_name, first_name, business_type, official_email, phone_number)
            st.success(f"Successfully updated: {business_name} to {new_business_name}")

    # Display updated data
    result2 = view_all_data()
    df2 = pd.DataFrame(result2, columns=['Business ID', 'Business Name','Last Name', 'First Name', 'Business Type', 'Official Email', 'Phone Number'])
    with st.expander("Updated Data"):
        st.dataframe(df2)
