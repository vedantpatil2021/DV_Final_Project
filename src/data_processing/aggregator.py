import pandas as pd
import numpy as np
import streamlit as st
import config
from src.data_processing.loader import get_country_codes

@st.cache_data
def aggregate_by_year(df, column='Total'):
    if df.empty or column not in df.columns:
        return pd.DataFrame()
    
    aggregated = df.groupby('Year')[column].sum().reset_index()
    return aggregated

@st.cache_data
def aggregate_by_region(df, column='Total', year=None):
    if df.empty or column not in df.columns:
        return pd.DataFrame()
    
    if year is not None:
        df = df[df['Year'] == year]
    
    region_map = {}
    for region, countries in config.REGIONS.items():
        for country_code in countries:
            region_map[country_code] = region
    
    df_with_region = df.copy()
    df_with_region['Region'] = df_with_region['ISO 3166-1 alpha-3'].map(region_map)
    
    df_with_region = df_with_region.dropna(subset=['Region'])
    
    aggregated = df_with_region.groupby('Region')[column].sum().reset_index()
    return aggregated

@st.cache_data
def aggregate_by_source(df, year=None, country=None):
    if df.empty:
        return pd.DataFrame()
    
    source_columns = ["Coal", "Oil", "Gas", "Cement", "Flaring", "Other"]
    
    source_columns = [col for col in source_columns if col in df.columns]
    if not source_columns:
        return pd.DataFrame()
    
    filtered_df = df.copy()
    if year is not None:
        filtered_df = filtered_df[filtered_df['Year'] == year]
    if country is not None:
        filtered_df = filtered_df[filtered_df['Country'] == country]
    
    if country is not None:
        result = filtered_df[['Year'] + source_columns]
    else:
        result = pd.DataFrame({
            'Source': source_columns,
            'Emissions': [filtered_df[col].sum() for col in source_columns]
        })
    
    return result

@st.cache_data
def calculate_per_source_percentages(df, year=None):
    if df.empty:
        return pd.DataFrame()
    
    source_columns = ["Coal", "Oil", "Gas", "Cement", "Flaring", "Other"]
    
    source_columns = [col for col in source_columns if col in df.columns]
    if not source_columns:
        return pd.DataFrame()
    
    if year is not None:
        df = df[df['Year'] == year]
    
    sources_by_year = df.groupby('Year')[source_columns].sum().reset_index()
    
    for source in source_columns:
        sources_by_year[f"{source}_pct"] = (sources_by_year[source] / sources_by_year[source_columns].sum(axis=1)) * 100
    
    return sources_by_year

@st.cache_data
def get_top_emitters(df, column='Total', year=None, n=10):
    if df.empty or column not in df.columns:
        return pd.DataFrame()
    
    if year is not None:
        df = df[df['Year'] == year]
    
    top_n = df.sort_values(column, ascending=False).head(n)
    return top_n

@st.cache_data
def calculate_growth_rates(df, column='Total', periods=[5, 10, 20]):
    if df.empty or column not in df.columns:
        return pd.DataFrame()
    
    latest_year = df['Year'].max()
    
    result = pd.DataFrame({'Country': df['Country'].unique()})
    
    for period in periods:
        current_year_data = df[df['Year'] == latest_year][['Country', column]].set_index('Country')
        past_year_data = df[df['Year'] == (latest_year - period)][['Country', column]].set_index('Country')
        
        growth = pd.DataFrame({
            'Country': current_year_data.index,
            f'{period}yr_growth': ((current_year_data[column] / past_year_data[column]) - 1) * 100
        }).set_index('Country')
        
        result = result.set_index('Country').join(growth, how='left').reset_index()
    
    return result