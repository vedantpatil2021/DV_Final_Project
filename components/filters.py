import streamlit as st
import config

def add_source_filter(available_sources, default_all=True):
    default_selection = available_sources if default_all else []
    
    selected_sources = st.sidebar.multiselect(
        "Select Emission Sources",
        options=available_sources,
        default=default_selection
    )
    
    return selected_sources

def add_region_filter(default_selection=None):
    available_regions = list(config.REGIONS.keys())
    
    if default_selection is None:
        default_selection = ["North America", "Europe", "Asia"]
    
    default_selection = [r for r in default_selection if r in available_regions]
    
    selected_regions = st.sidebar.multiselect(
        "Select Regions",
        options=available_regions,
        default=default_selection
    )
    
    return selected_regions

def add_multi_country_selector(df, default_selection=None, max_selections=10):
    available_countries = sorted(df['Country'].unique())
    
    if default_selection is None:
        default_selection = ["China", "United States", "India", "Russia", "Japan"]
    
    default_selection = [c for c in default_selection if c in available_countries]
    
    selected_countries = st.sidebar.multiselect(
        "Select Countries (max {})".format(max_selections),
        options=available_countries,
        default=default_selection
    )
    
    if len(selected_countries) > max_selections:
        st.sidebar.warning(f"You've selected {len(selected_countries)} countries. For better visualization, please limit your selection to {max_selections} countries.")
        selected_countries = selected_countries[:max_selections]
    
    return selected_countries

def add_metric_selector(metrics, default="Total"):
    if default not in metrics:
        default = metrics[0]
    
    selected_metric = st.sidebar.selectbox(
        "Select Metric",
        options=metrics,
        index=metrics.index(default) if default in metrics else 0
    )
    
    return selected_metric

def add_normalization_toggle(default=False):
    normalize = st.sidebar.checkbox(
        "Normalize Data (% of Max)",
        value=default
    )
    
    return normalize