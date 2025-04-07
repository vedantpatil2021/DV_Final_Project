import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import numpy as np
import config

def create_choropleth_map(df, iso_col, color_col, title, **kwargs):
    default_kwargs = {
        'height': config.DEFAULT_MAP_HEIGHT,
        'color_continuous_scale': config.CHOROPLETH_COLORSCALE,
        'labels': {color_col: color_col.replace('_', ' ').title()},
        'template': 'plotly_white',
        'projection': 'natural earth'
    }
    
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.choropleth(
        df,
        locations=iso_col,
        color=color_col,
        title=title,
        **kwargs
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        geo=dict(
            showcoastlines=True,
            coastlinecolor="Black",
            showland=True,
            landcolor="lightgray",
            showocean=True,
            oceancolor="aliceblue",
            showlakes=True,
            lakecolor="aliceblue",
            showrivers=True,
            rivercolor="aliceblue"
        )
    )
    
    return fig

def create_bubble_map(df, lat_col, lon_col, size_col, hover_name_col, title, color_col=None, **kwargs):
    default_kwargs = {
        'height': config.DEFAULT_MAP_HEIGHT,
        'template': 'plotly_white',
        'labels': {size_col: size_col.replace('_', ' ').title()},
        'projection': 'natural earth'
    }
    
    kwargs = {**default_kwargs, **kwargs}
    
    if color_col:
        fig = px.scatter_geo(
            df,
            lat=lat_col,
            lon=lon_col,
            size=size_col,
            hover_name=hover_name_col,
            color=color_col,
            title=title,
            **kwargs
        )
    else:
        fig = px.scatter_geo(
            df,
            lat=lat_col,
            lon=lon_col,
            size=size_col,
            hover_name=hover_name_col,
            title=title,
            **kwargs
        )
    
    # Common layout adjustments
    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        geo=dict(
            showcoastlines=True,
            coastlinecolor="Black",
            showland=True,
            landcolor="lightgray",
            showocean=True,
            oceancolor="aliceblue",
            showlakes=True,
            lakecolor="aliceblue",
            showrivers=True,
            rivercolor="aliceblue"
        )
    )
    
    return fig

def create_regional_choropleth(df, region_col, color_col, title, **kwargs):
    default_kwargs = {
        'height': config.DEFAULT_MAP_HEIGHT,
        'color_continuous_scale': config.CHOROPLETH_COLORSCALE,
        'labels': {color_col: color_col.replace('_', ' ').title()},
        'template': 'plotly_white',
        'projection': 'natural earth',
        'scope': 'world'
    }
    
    kwargs = {**default_kwargs, **kwargs}

    fig = px.choropleth(
        df,
        locations=region_col,
        locationmode="country names",
        color=color_col,
        title=title,
        **kwargs
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        geo=dict(
            showcoastlines=True,
            coastlinecolor="Black",
            showland=True,
            landcolor="lightgray",
            showocean=True,
            oceancolor="aliceblue",
            showlakes=True,
            lakecolor="aliceblue",
            showrivers=True,
            rivercolor="aliceblue"
        )
    )
    
    return fig

def animate_choropleth_by_year(df, iso_col, color_col, year_col, title, **kwargs):
    default_kwargs = {
        'height': config.DEFAULT_MAP_HEIGHT,
        'color_continuous_scale': config.CHOROPLETH_COLORSCALE,
        'labels': {color_col: color_col.replace('_', ' ').title()},
        'template': 'plotly_white',
        'projection': 'natural earth',
        'animation_frame': year_col,
        'range_color': [df[color_col].min(), df[color_col].max()]
    }
    
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.choropleth(
        df,
        locations=iso_col,
        color=color_col,
        title=title,
        **kwargs
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        geo=dict(
            showcoastlines=True,
            coastlinecolor="Black",
            showland=True,
            landcolor="lightgray",
            showocean=True,
            oceancolor="aliceblue",
            showlakes=True,
            lakecolor="aliceblue",
            showrivers=True,
            rivercolor="aliceblue"
        )
    )
    
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 800
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 300
    
    return fig