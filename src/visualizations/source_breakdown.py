import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import numpy as np
import config

def create_pie_chart(labels, values, title, **kwargs):
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'color': labels,
        'color_discrete_map': config.EMISSION_SOURCES_COLORS if set(labels).issubset(config.EMISSION_SOURCES_COLORS.keys()) else None,
        'hole': 0.3
    }
    
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.pie(
        names=labels,
        values=values,
        title=title,
        **kwargs
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color='white', width=2))
    )
    
    return fig

def create_donut_chart(labels, values, title, **kwargs):
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'color': labels,
        'color_discrete_map': config.EMISSION_SOURCES_COLORS if set(labels).issubset(config.EMISSION_SOURCES_COLORS.keys()) else None,
        'hole': 0.6
    }
    
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.pie(
        names=labels,
        values=values,
        title=title,
        **kwargs
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color='white', width=2))
    )
    
    fig.update_layout(
        annotations=[dict(
            text=f'Total<br>{sum(values):,.0f}',
            x=0.5, y=0.5,
            font_size=14,
            showarrow=False
        )]
    )
    
    return fig

def create_treemap(df, path, values, title, **kwargs):
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'color_discrete_map': config.EMISSION_SOURCES_COLORS if path[-1] in df.columns and set(df[path[-1]].unique()).issubset(config.EMISSION_SOURCES_COLORS.keys()) else None,
    }
    
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.treemap(
        df,
        path=path,
        values=values,
        title=title,
        **kwargs
    )
    
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Value: %{value:,.2f}<br>Percentage: %{percentRoot:.2%}<extra></extra>'
    )
    
    return fig

def create_sunburst(df, path, values, title, **kwargs):
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'color_discrete_map': config.EMISSION_SOURCES_COLORS if path[-1] in df.columns and set(df[path[-1]].unique()).issubset(config.EMISSION_SOURCES_COLORS.keys()) else None,
    }
    
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.sunburst(
        df,
        path=path,
        values=values,
        title=title,
        **kwargs
    )
    
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Value: %{value:,.2f}<br>Percentage: %{percentRoot:.2%}<extra></extra>'
    )
    
    return fig

def create_stacked_bar_by_source(df, x_col, title, normalize=False, **kwargs):
    source_columns = ["Coal", "Oil", "Gas", "Cement", "Flaring", "Other"]
    
    available_sources = [s for s in source_columns if s in df.columns]
    
    if df.empty or not available_sources:
        fig = go.Figure()
        fig.update_layout(
            title=title,
            height=config.DEFAULT_CHART_HEIGHT,
            template='plotly_white',
            annotations=[dict(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False
            )]
        )
        return fig
    
    if normalize:
        df['Total_Sources'] = df[available_sources].sum(axis=1)
        
        for source in available_sources:
            df[f"{source}_pct"] = (df[source] / df['Total_Sources']) * 100
        
        value_cols = [f"{source}_pct" for source in available_sources]
        y_title = "Percentage (%)"
    else:
        value_cols = available_sources
        y_title = "Emissions (Million Tonnes CO2)"
    
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'barmode': 'stack',
        'color_discrete_map': {source: config.EMISSION_SOURCES_COLORS.get(source.replace('_pct', ''), '#000000') for source in value_cols}
    }
    
    kwargs = {**default_kwargs, **kwargs}
    
    fig = go.Figure()
    
    for i, source in enumerate(value_cols):
        source_name = source.replace('_pct', '')
        fig.add_trace(go.Bar(
            x=df[x_col],
            y=df[source],
            name=source_name,
            marker_color=kwargs['color_discrete_map'].get(source_name, '#000000')
        ))
    
    fig.update_layout(
        title=title,
        height=kwargs['height'],
        template=kwargs['template'],
        barmode=kwargs['barmode'],
        legend_title="Source",
        xaxis_title=x_col.replace('_', ' ').title(),
        yaxis_title=y_title
    )
    
    return fig

def create_source_heatmap(df, title, **kwargs):
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'color_continuous_scale': 'Viridis',
        'aspect': 'auto',
        'labels': {'color': 'Intensity'}
    }
    
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.imshow(
        df,
        title=title,
        **kwargs
    )
    
    fig.update_layout(
        xaxis_title="Emission Source",
        yaxis_title="Category"
    )
    
    annotations = []
    for i, row in enumerate(df.index):
        for j, col in enumerate(df.columns):
            annotations.append(dict(
                x=j,
                y=i,
                text=f"{df.iloc[i, j]:.1f}",
                font=dict(color='white' if df.iloc[i, j] > df.values.mean() else 'black'),
                showarrow=False
            ))
    
    fig.update_layout(annotations=annotations)
    
    return fig

def create_source_intensity_scatter(df, source_col, total_col, label_col, title, **kwargs):
    df = df.copy()
    df['intensity'] = (df[source_col] / df[total_col]) * 100
    
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {
            'intensity': f"{source_col} Intensity (%)", 
            total_col: total_col.replace('_', ' ').title()
        },
        'hover_name': label_col,
        'size': total_col,
        'color': 'intensity',
        'color_continuous_scale': 'Viridis',
        'opacity': 0.7,
        'size_max': 50
    }
    
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.scatter(
        df,
        x=total_col,
        y='intensity',
        title=title,
        **kwargs
    )
    
    avg_intensity = df['intensity'].mean()
    fig.add_hline(
        y=avg_intensity,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Avg: {avg_intensity:.1f}%",
        annotation_position="top right"
    )
    
    for i, row in df.iterrows():
        if (row['intensity'] > avg_intensity * 1.5) or (row['intensity'] < avg_intensity * 0.5):
            fig.add_annotation(
                x=row[total_col],
                y=row['intensity'],
                text=row[label_col],
                showarrow=True,
                arrowhead=1
            )
    
    return fig

def create_source_comparison_spider(df, category_col, source_cols, title):
    if category_col not in df.columns or not all(col in df.columns for col in source_cols):
        fig = go.Figure()
        fig.update_layout(
            title=title,
            height=config.DEFAULT_CHART_HEIGHT,
            template='plotly_white',
            annotations=[dict(
                text="Required columns not available",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False
            )]
        )
        return fig
    
    fig = go.Figure()
    
    categories = df[category_col].tolist()
    
    df_norm = df.copy()
    for col in source_cols:
        max_val = df[col].max()
        if max_val > 0: 
            df_norm[col] = (df[col] / max_val) * 100
    
    for source in source_cols:
        fig.add_trace(go.Scatterpolar(
            r=df_norm[source].tolist(),
            theta=categories,
            fill='toself',
            name=source,
            line_color=config.EMISSION_SOURCES_COLORS.get(source, None)
        ))
    
    fig.update_layout(
        title=title,
        height=config.DEFAULT_CHART_HEIGHT,
        template='plotly_white',
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        )
    )
    
    return fig