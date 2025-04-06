import pandas as pd
import numpy as np
import streamlit as st

def format_number(value, precision=1, suffix=''):
    if pd.isna(value) or value is None:
        return "N/A"
    
    formatted = f"{value:,.{precision}f}"
    
    if suffix:
        formatted += f" {suffix}"
    
    return formatted

def format_with_units(value, unit='Mt CO2'):
    if pd.isna(value) or value is None:
        return "N/A"
    
    if abs(value) >= 1e9:
        return f"{value/1e9:.1f} G{unit}"
    elif abs(value) >= 1e6:
        return f"{value/1e6:.1f} M{unit}"
    elif abs(value) >= 1e3:
        return f"{value/1e3:.1f} k{unit}"
    else:
        return f"{value:.1f} {unit}"

def format_percent(value, precision=1, include_sign=False):
    if pd.isna(value) or value is None:
        return "N/A"
    
    if include_sign and value > 0:
        return f"+{value:.{precision}f}%"
    else:
        return f"{value:.{precision}f}%"

def format_year_range(start_year, end_year):
    return f"{start_year}–{end_year}"

def format_country_name(country_code):
    country_mapping = {
        'USA': 'United States',
        'CHN': 'China',
        'IND': 'India',
        'RUS': 'Russia',
        'JPN': 'Japan',
        'DEU': 'Germany',
        'GBR': 'United Kingdom',
        'FRA': 'France',
        'ITA': 'Italy',
        'CAN': 'Canada',
        'BRA': 'Brazil',
        'AUS': 'Australia'
    }
    
    return country_mapping.get(country_code, country_code)

def format_metric_for_display(metric, value, show_units=True):
    if pd.isna(value) or value is None:
        return "N/A"
    
    if 'percent' in metric.lower() or metric.endswith('_pct'):
        return format_percent(value)
    elif any(term in metric.lower() for term in ['total', 'emissions', 'coal', 'oil', 'gas', 'cement']):
        return format_with_units(value, unit='Mt CO2' if show_units else '')
    elif 'per_capita' in metric.lower():
        return format_with_units(value, unit='t CO2/capita' if show_units else '')
    else:
        return format_number(value)

def create_delta_indicator(current, previous, is_good_if_down=True):
    if pd.isna(current) or pd.isna(previous) or previous == 0:
        return None, None
    
    delta = ((current - previous) / previous) * 100
    
    if delta < 0:
        is_positive = is_good_if_down
    elif delta > 0:
        is_positive = not is_good_if_down
    else:
        is_positive = None
    
    return delta, is_positive

def abbreviate_large_number(num):
    if pd.isna(num) or num is None:
        return "N/A"
    
    magnitude = 0
    abbreviations = ['', 'K', 'M', 'B', 'T']
    while abs(num) >= 1000 and magnitude < len(abbreviations) - 1:
        magnitude += 1
        num /= 1000.0
    
    if magnitude > 0:
        return f"{num:.1f}{abbreviations[magnitude]}"
    else:
        return f"{num:.0f}"