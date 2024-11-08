import streamlit as st
from database import add_data

def create():
    col1, col2 = st.columns(2)
    with col1:
        b_id = st.text_input("Business ID:")
        b_name = st.text_input("Business Name:")
        l_name = st.text_input("Legal Name:")
        f_name = st.text_input("Founder Name:")
    with col2:
        b_type = st.selectbox("Business Type", ["Fashion", "Travel", "Sports", "Food"])  # Adjust as needed
        oo_mail = st.text_input("Official E-mail:")
        phone = st.text_input("Phone Number:")

    if st.button("Add Business"):
        # Call the add_data function with the inputs for the Business table
        add_data(b_id, b_name, l_name, f_name, b_type, oo_mail, phone)
        st.success(f"Successfully added Business: {b_name}")
