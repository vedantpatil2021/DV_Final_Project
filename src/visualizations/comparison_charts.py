import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import config

def create_bar_comparison(df, category_col, value_col, title, **kwargs):
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {value_col: value_col.replace('_', ' ').title(), category_col: ''},
        'color': value_col,
        'color_continuous_scale': config.CHOROPLETH_COLORSCALE,
        'text_auto': '.2s'
    }
    
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.bar(
        df,
        x=category_col,
        y=value_col,
        title=title,
        **kwargs
    )
    
    fig.update_layout(
        xaxis={'categoryorder': 'total descending'}
    )
    
    return fig

def create_horizontal_bar_comparison(df, category_col, value_col, title, **kwargs):
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {value_col: value_col.replace('_', ' ').title(), category_col: ''},
        'color': value_col,
        'color_continuous_scale': config.CHOROPLETH_COLORSCALE,
        'text_auto': '.2s',
        'orientation': 'h'
    }
    
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.bar(
        df,
        y=category_col,
        x=value_col,
        title=title,
        **kwargs
    )
    
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

def create_grouped_bar_chart(df, category_col, value_cols, title, **kwargs):
    melted_df = pd.melt(
        df, 
        id_vars=[category_col], 
        value_vars=value_cols,
        var_name='Metric', 
        value_name='Value'
    )
    
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {'Value': 'Value', 'Metric': 'Metric'},
        'barmode': 'group',
        'text_auto': '.2s'
    }
    
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.bar(
        melted_df,
        x=category_col,
        y='Value',
        color='Metric',
        title=title,
        **kwargs
    )
    
    return fig

def create_scatter_comparison(df, x_col, y_col, title, hover_name=None, size_col=None, color_col=None, **kwargs):
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {
            x_col: x_col.replace('_', ' ').title(), 
            y_col: y_col.replace('_', ' ').title()
        },
        'opacity': 0.7
    }
    
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        hover_name=hover_name,
        size=size_col,
        color=color_col,
        title=title,
        **kwargs
    )
    
    return fig

def create_bubble_chart(df, x_col, y_col, size_col, title, hover_name=None, color_col=None, **kwargs):
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {
            x_col: x_col.replace('_', ' ').title(), 
            y_col: y_col.replace('_', ' ').title(),
            size_col: size_col.replace('_', ' ').title()
        },
        'opacity': 0.7,
        'size_max': 60
    }
    
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        size=size_col,
        hover_name=hover_name,
        color=color_col,
        title=title,
        **kwargs
    )
    
    return fig

def create_multi_metric_radar_chart(df, category_col, value_cols, title):
    categories = df[category_col].tolist()
    
    fig = go.Figure()
    
    for col in value_cols:
        fig.add_trace(go.Scatterpolar(
            r=df[col].tolist(),
            theta=categories,
            fill='toself',
            name=col.replace('_', ' ').title()
        ))
    
    fig.update_layout(
        title=title,
        height=config.DEFAULT_CHART_HEIGHT,
        template='plotly_white',
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max([df[col].max() for col in value_cols]) * 1.1]
            )
        )
    )
    
    return fig