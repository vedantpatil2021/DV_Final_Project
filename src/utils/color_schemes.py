import plotly.express as px
import config

EMISSION_SOURCES_COLORS = config.EMISSION_SOURCES_COLORS

def get_categorical_colors(n_colors=10):
    if n_colors <= 10:
        return px.colors.qualitative.Plotly[:n_colors]
    elif n_colors <= 12:
        return px.colors.qualitative.Set3[:n_colors]
    else:
        base_colors = px.colors.qualitative.Plotly
        return [base_colors[i % len(base_colors)] for i in range(n_colors)]

def get_sequential_colorscale(colorscale_name=None):
    if colorscale_name is None:
        return config.CHOROPLETH_COLORSCALE

    if hasattr(px.colors.sequential, colorscale_name):
        return getattr(px.colors.sequential, colorscale_name)
    else:
        return config.CHOROPLETH_COLORSCALE

def get_diverging_colorscale(colorscale_name=None):
    if colorscale_name is None:
        return "RdBu_r"
    
    if hasattr(px.colors.diverging, colorscale_name):
        return getattr(px.colors.diverging, colorscale_name)
    else:
        return "RdBu_r"

def get_change_colorscale():
    return [
        [0, "rgb(165, 0, 38)"],    
        [0.25, "rgb(215, 48, 39)"],  
        [0.45, "rgb(244, 109, 67)"], 
        [0.5, "rgb(255, 255, 255)"],
        [0.55, "rgb(116, 173, 209)"],
        [0.75, "rgb(69, 117, 180)"], 
        [1, "rgb(49, 54, 149)"]
    ]

def get_region_colors():
    regions = list(config.REGIONS.keys())
    colors = get_categorical_colors(len(regions))
    
    return dict(zip(regions, colors))

def color_by_value(value, min_val, max_val, colorscale_name=None):
    import plotly.colors as pc
    
    colorscale = get_sequential_colorscale(colorscale_name)
    
    if max_val == min_val:
        normalized = 0.5 
    else:
        normalized = (value - min_val) / (max_val - min_val)

    normalized = max(0, min(1, normalized))

    return pc.sample_colorscale(colorscale, normalized)[0]