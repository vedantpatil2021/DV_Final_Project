import streamlit as st
import pandas as pd
import config

def add_year_range_selector(df, default_start=config.DEFAULT_START_YEAR, default_end=config.DEFAULT_END_YEAR):
    min_year = int(df['Year'].min())
    max_year = int(df['Year'].max())
    
    default_start = max(min_year, default_start)
    default_end = min(max_year, default_end)
    
    start_year = st.sidebar.slider(
        "Start Year",
        min_value=min_year,
        max_value=max_year,
        value=default_start,
        step=1
    )
    
    end_year = st.sidebar.slider(
        "End Year",
        min_value=start_year,
        max_value=max_year,
        value=min(default_end, max_year),
        step=1
    )
    
    return start_year, end_year

def add_year_selector(df, default=None, label="Select Year"):
    years = sorted(df['Year'].unique())
    
    if default is None:
        default = years[-1]  # Latest year
    elif default not in years:
        default = min(filter(lambda y: y >= default, years), default=years[-1])
    
    selected_year = st.sidebar.selectbox(
        label,
        options=years,
        index=years.index(default) if default in years else len(years) - 1
    )
    
    return selected_year

def add_country_selector(df, default="China"):
    countries = sorted(df['Country'].unique())
    
    if default not in countries:
        default = countries[0]
    
    selected_country = st.sidebar.selectbox(
        "Select Country",
        options=countries,
        index=countries.index(default) if default in countries else 0
    )
    
    return selected_country

def add_top_n_selector(default=10, max_value=50):
    top_n = st.sidebar.slider(
        "Number of items to display",
        min_value=5,
        max_value=max_value,
        value=default,
        step=5
    )
    
    return top_n