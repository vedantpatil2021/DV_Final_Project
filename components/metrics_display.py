import streamlit as st
import pandas as pd
import numpy as np

def display_kpi_card(title, value, previous_value=None, format_string="{:,.1f}", is_percent=False, is_good_if_up=True):
    if is_percent:
        formatted_value = format_string.format(value) + "%"
    else:
        formatted_value = format_string.format(value)
    
    st.markdown(
        f"""
        <div style="
            padding: 15px;
            border-radius: 5px;
            background-color: #f0f2f6;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 10px;">
            <h3 style="margin-top: 0;">{title}</h3>
            <p style="font-size: 24px; font-weight: bold; margin: 0;">{formatted_value}</p>
            {get_trend_html(value, previous_value, is_good_if_up) if previous_value is not None else ""}
        </div>
        """, 
        unsafe_allow_html=True
    )

def get_trend_html(current, previous, is_good_if_up):
    if current == previous:
        return '<p style="color: gray; margin: 0;">No change</p>'
    
    change = ((current - previous) / previous) * 100
    is_increase = current > previous
    
    if is_increase:
        color = "green" if is_good_if_up else "red"
        arrow = "↑"
    else:
        color = "red" if is_good_if_up else "green"
        arrow = "↓"
    
    return f'<p style="color: {color}; margin: 0;">{arrow} {abs(change):.1f}%</p>'

def display_metric_row(metrics_data):
    columns = st.columns(len(metrics_data))
    
    for i, metric in enumerate(metrics_data):
        with columns[i]:
            display_kpi_card(
                title=metric['title'],
                value=metric['value'],
                previous_value=metric.get('previous_value'),
                format_string=metric.get('format_string', "{:,.1f}"),
                is_percent=metric.get('is_percent', False),
                is_good_if_up=metric.get('is_good_if_up', True)
            )

def display_change_summary(df, column, start_year, end_year, title=None):
    if title:
        st.subheader(title)
    
    start_value = df[df['Year'] == start_year][column].sum()
    end_value = df[df['Year'] == end_year][column].sum()
    
    absolute_change = end_value - start_value
    percent_change = (absolute_change / start_value) * 100 if start_value != 0 else np.inf
    
    years_diff = end_year - start_year
    avg_annual_percent = ((end_value / start_value) ** (1 / years_diff) - 1) * 100 if start_value != 0 and years_diff > 0 else 0
    
    metrics = [
        {
            'title': f"{column} in {start_year}",
            'value': start_value,
            'format_string': "{:,.2f}"
        },
        {
            'title': f"{column} in {end_year}",
            'value': end_value,
            'format_string': "{:,.2f}"
        },
        {
            'title': "Total Change",
            'value': percent_change,
            'format_string': "{:+.2f}",
            'is_percent': True,
            'is_good_if_up': False
        },
        {
            'title': "Avg. Annual Change",
            'value': avg_annual_percent,
            'format_string': "{:+.2f}",
            'is_percent': True,
            'is_good_if_up': False 
        }
    ]
    
    display_metric_row(metrics)