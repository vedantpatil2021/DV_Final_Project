import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import config

def create_line_chart(df, x_col, y_col, title, color_col=None, **kwargs):
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {y_col: y_col.replace('_', ' ').title(), x_col: x_col.replace('_', ' ').title()},
        'hover_data': None
    }
    
    kwargs = {**default_kwargs, **kwargs}
    
    if color_col:
        fig = px.line(df, x=x_col, y=y_col, color=color_col, title=title, **kwargs)
    else:
        fig = px.line(df, x=x_col, y=y_col, title=title, **kwargs)
    
    fig.update_layout(
        hovermode="x unified",
        xaxis=dict(tickmode='linear', dtick=5) if x_col == 'Year' else None
    )
    
    return fig

def create_multi_line_chart(df, x_col, y_cols, title, **kwargs):
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {col: col.replace('_', ' ').title() for col in y_cols},
        'hover_data': None
    }
    
    kwargs = {**default_kwargs, **kwargs}
    
    fig = go.Figure()
    
    for col in y_cols:
        fig.add_trace(
            go.Scatter(
                x=df[x_col], 
                y=df[col], 
                name=col,
                mode='lines'
            )
        )
    
    fig.update_layout(
        title=title,
        height=kwargs['height'],
        template=kwargs['template'],
        hovermode="x unified",
        xaxis=dict(tickmode='linear', dtick=5) if x_col == 'Year' else None,
        xaxis_title=x_col.replace('_', ' ').title(),
        yaxis_title=y_cols[0].replace('_', ' ').title()  # Use first y column for axis title
    )
    
    return fig

def create_area_chart(df, x_col, y_col, title, color_col=None, **kwargs):
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {y_col: y_col.replace('_', ' ').title(), x_col: x_col.replace('_', ' ').title()},
        'hover_data': None
    }
    
    kwargs = {**default_kwargs, **kwargs}
    
    if color_col:
        fig = px.area(df, x=x_col, y=y_col, color=color_col, title=title, **kwargs)
    else:
        fig = px.area(df, x=x_col, y=y_col, title=title, **kwargs)
    
    fig.update_layout(
        hovermode="x unified",
        xaxis=dict(tickmode='linear', dtick=5) if x_col == 'Year' else None
    )
    
    return fig

def create_stacked_area_chart(df, x_col, y_cols, title, **kwargs):
    melted_df = pd.melt(
        df, 
        id_vars=[x_col], 
        value_vars=y_cols,
        var_name='Category', 
        value_name='Value'
    )
    
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {'Value': 'Value', 'Category': 'Category'},
        'color_discrete_map': config.EMISSION_SOURCES_COLORS if set(y_cols).issubset(config.EMISSION_SOURCES_COLORS.keys()) else None
    }
    
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.area(
        melted_df, 
        x=x_col, 
        y='Value', 
        color='Category', 
        title=title,
        **kwargs
    )
    
    fig.update_layout(
        hovermode="x unified",
        xaxis=dict(tickmode='linear', dtick=5) if x_col == 'Year' else None
    )
    
    return fig

def create_bar_chart_with_average_line(df, x_col, y_col, title, avg_label="Average", **kwargs):
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {y_col: y_col.replace('_', ' ').title(), x_col: x_col.replace('_', ' ').title()},
        'hover_data': None
    }
    
    kwargs = {**default_kwargs, **kwargs}
    
    avg = df[y_col].mean()
    
    fig = px.bar(df, x=x_col, y=y_col, title=title, **kwargs)
    
    fig.add_trace(
        go.Scatter(
            x=df[x_col],
            y=[avg] * len(df),
            mode='lines',
            name=avg_label,
            line=dict(color='red', width=2, dash='dash')
        )
    )
    
    fig.update_layout(
        hovermode="x unified",
        xaxis=dict(tickmode='linear', dtick=5) if x_col == 'Year' else None
    )
    
    return fig

def highlight_years_of_interest(fig, years_dict):
    for year, event in years_dict.items():
        fig.add_vline(
            x=year,
            line_dash="dash",
            line_color="rgba(0, 0, 0, 0.5)",
            annotation_text=event,
            annotation_position="top right"
        )
    
    return fig