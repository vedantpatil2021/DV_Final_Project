"""
Custom metrics calculations for the CO2 emissions dashboard.
"""

import pandas as pd
import numpy as np
import streamlit as st

def calculate_percent_change(df, column, year1, year2):
    value1 = df[df['Year'] == year1][column].sum()
    value2 = df[df['Year'] == year2][column].sum()
    
    if value1 == 0:
        return np.inf if value2 > 0 else -np.inf if value2 < 0 else 0
    
    return ((value2 - value1) / value1) * 100

@st.cache_data
def calculate_cagr(df, column, start_year, end_year):
    start_value = df[df['Year'] == start_year][column].sum()
    end_value = df[df['Year'] == end_year][column].sum()
    
    n_years = end_year - start_year
    
    if start_value <= 0 or n_years <= 0:
        return 0
    
    cagr = (((end_value / start_value) ** (1 / n_years)) - 1) * 100
    
    return cagr

@st.cache_data
def calculate_moving_average(df, column, window=5):
    df = df.sort_values('Year')
    
    return df[column].rolling(window=window, min_periods=1).mean()

@st.cache_data
def calculate_emission_intensity(df, source_col, total_col):
    intensity = (df[source_col] / df[total_col]) * 100
    
    intensity = intensity.replace([np.inf, -np.inf, np.nan], 0)
    
    return intensity

@st.cache_data
def calculate_top_contributors(df, column, year, n=10, min_value=None):
    year_df = df[df['Year'] == year].copy()
    
    # Apply minimum value filter if specified
    if min_value is not None:
        year_df = year_df[year_df[column] >= min_value]
    
    top_n = year_df.sort_values(column, ascending=False).head(n)
    
    total = year_df[column].sum()
    if total > 0:
        top_n['Percentage'] = (top_n[column] / total) * 100
    else:
        top_n['Percentage'] = 0
    
    return top_n

@st.cache_data
def calculate_reduction_needed(df, column, current_year, target_year, target_reduction_pct):
    current_emissions = df[df['Year'] == current_year][column].sum()
    
    target_emissions = current_emissions * (1 - (target_reduction_pct / 100))
    
    absolute_reduction = current_emissions - target_emissions
    
    years_remaining = target_year - current_year
    if years_remaining <= 0:
        annual_reduction = absolute_reduction
        annual_reduction_pct = target_reduction_pct
    else:
        annual_reduction = absolute_reduction / years_remaining
        annual_reduction_pct = (1 - ((1 - (target_reduction_pct / 100)) ** (1 / years_remaining))) * 100
    
    return {
        'current_emissions': current_emissions,
        'target_emissions': target_emissions,
        'absolute_reduction': absolute_reduction,
        'annual_reduction': annual_reduction,
        'annual_reduction_pct': annual_reduction_pct
    }