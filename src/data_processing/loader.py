import pandas as pd
import streamlit as st
import os
import json
import config

@st.cache_data
def load_emissions_data():
    try:
        if not os.path.exists(config.TOTAL_EMISSIONS_FILE):
            st.error(f"Error: Data file not found at {config.TOTAL_EMISSIONS_FILE}")
            return pd.DataFrame()
        
        df = pd.read_csv(config.TOTAL_EMISSIONS_FILE)
        
        required_columns = ['Country', 'ISO 3166-1 alpha-3', 'Year', 'Total']
        for col in required_columns:
            if col not in df.columns:
                st.error(f"Error: Required column '{col}' not found in data")
                return pd.DataFrame()
        
        df['Year'] = df['Year'].astype(int)
        
        return df
    
    except Exception as e:
        st.error(f"Error loading emissions data: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_per_capita_data():
    try:
        if not os.path.exists(config.PER_CAPITA_EMISSIONS_FILE):
            st.error(f"Error: Data file not found at {config.PER_CAPITA_EMISSIONS_FILE}")
            return pd.DataFrame()
        
        df = pd.read_csv(config.PER_CAPITA_EMISSIONS_FILE)
        
        required_columns = ['Country', 'ISO 3166-1 alpha-3', 'Year', 'Total']
        for col in required_columns:
            if col not in df.columns:
                st.error(f"Error: Required column '{col}' not found in data")
                return pd.DataFrame()
        
        df['Year'] = df['Year'].astype(int)
        
        return df
    
    except Exception as e:
        st.error(f"Error loading per capita data: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_sources_data():
    try:
        if not os.path.exists(config.SOURCES_FILE):
            st.error(f"Error: Data file not found at {config.SOURCES_FILE}")
            return pd.DataFrame()
        
        df = pd.read_csv(config.SOURCES_FILE)
        
        required_columns = ['Country', 'ISO 3166-1 alpha-3', 'Year']
        for col in required_columns:
            if col not in df.columns:
                st.error(f"Error: Required column '{col}' not found in data")
                return pd.DataFrame()
        
        df['Year'] = df['Year'].astype(int)
        
        return df
    
    except Exception as e:
        st.error(f"Error loading sources data: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_metadata(metadata_file):
    try:
        if not os.path.exists(metadata_file):
            st.warning(f"Metadata file not found at {metadata_file}")
            return {}
        
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        return metadata
    
    except Exception as e:
        st.warning(f"Error loading metadata: {str(e)}")
        return {}

def get_country_codes():
    df = load_emissions_data()
    if df.empty:
        return {}
    
    country_codes = dict(zip(df['Country'], df['ISO 3166-1 alpha-3']))
    return country_codes

def get_countries_by_region():
    country_codes = get_country_codes()
    if not country_codes:
        return {}
    
    code_to_country = {code: country for country, code in country_codes.items()}
    
    countries_by_region = {}
    for region, codes in config.REGIONS.items():
        countries_by_region[region] = [code_to_country.get(code, code) for code in codes if code in code_to_country]
    
    return countries_by_region