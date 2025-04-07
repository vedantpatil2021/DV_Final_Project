import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config

st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():    
    st.title(config.APP_TITLE)
    st.markdown(config.APP_DESCRIPTION)
    
    st.markdown("## Data Source")
    st.write(
        "The data used in this dashboard comes from the Global Carbon Budget 2022 "
        "published by the Global Carbon Project.<br>"
        "Dataset link: [Kaggle](https://www.kaggle.com/datasets/thedevastator/global-fossil-co2-emissions-by-country-2002-2022?resource=download)",unsafe_allow_html=True
    )
    
    st.markdown("## Available Datasets")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Total Emissions")
        st.write("Total CO2 emissions in millions of tonnes")
        
    with col2:
        st.markdown("### Per Capita Emissions")
        st.write("CO2 emissions in tonnes per capita")

    st.markdown("### Project by")
    st.markdown("""
    - Vedant Patil  
    - Parag Padekar  
    - Bhavika Jain  
    - Elnaz Nowrouzi
    """)


if __name__ == "__main__":
    main()