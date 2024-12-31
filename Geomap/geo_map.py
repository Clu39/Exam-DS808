import pandas as pd
import plotly.express as px
import json

# Data from the table
data = {
    "Region": ["Region Hovedstaden", "Region Sjælland", "Region Syddanmark", 
               "Region Midtjylland", "Region Nordjylland"],
    "Women": [1119, 466, 547, 557, 184]  # 2023
}

# Create a DataFrame
df = pd.DataFrame(data)

# Load GeoJSON file for Denmark regions
with open("regioner_geo1.json", "r") as f:
    geojson = json.load(f)

# Create a choropleth map
fig = px.choropleth_mapbox(
    df,
    geojson=geojson,
    locations="Region",  # Column in DataFrame
    featureidkey="properties.name",  # Key in GeoJSON file for region names
    color="Women",  # Column to visualize
    color_continuous_scale="Blues",  # Choose a color scale
    title="Stays and Residents at Women's Shelters (2023) - Women",
    mapbox_style="carto-positron",  # Base map style
    center={"lat": 56.26392, "lon": 9.501785},  # Center the map on Denmark
    zoom=5  # Adjust zoom level
)

# Show the figure
fig.show()
