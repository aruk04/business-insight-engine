import pandas as pd
import streamlit as st
import plotly.express as px
from database import view_all_data

def read():
    result = view_all_data()
    # Convert the result into a DataFrame with appropriate columns
    df = pd.DataFrame(result, columns=['Business ID', 'Business Name', 'Legal Name', 'Founder Name', 'Business Type', 'Official Email', 'Phone Number'])
    
    with st.expander("View all Businesses"):
        st.dataframe(df)
    
    with st.expander("Business Type Distribution"):
        # Count the number of businesses by type
        business_type_df = df['Business Type'].value_counts().reset_index()
        business_type_df.columns = ['Business Type', 'Count']
        st.dataframe(business_type_df)

        # Bar chart for business type distribution
        bar_chart = px.bar(business_type_df, x='Business Type', y='Count', title="Number of Businesses by Type", color='Business Type')
        st.plotly_chart(bar_chart)

