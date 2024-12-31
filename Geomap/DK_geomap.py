import plotly.express as px
import json
import pandas as pd

# Load the filtered GeoJSON (https://cartographyvectors.com/map/1434-denmark-with-regions)
with open("filtered_denmark_regions.geojson", "r") as file:
    filtered_geojson = json.load(file)

# Danish to English region name mapping
region_mapping = {
    "Region Hovedstaden": "Capital Region of Denmark",
    "Region Sjælland": "Region Zealand",
    "Region Syddanmark": "Region of Southern Denmark",
    "Region Midtjylland": "Central Denmark Region",
    "Region Nordjylland": "North Denmark Region"
}

# Data for 2017-2023 stays
shelter_data = {
    "Region": ["Region Hovedstaden", "Region Sjælland", "Region Syddanmark", "Region Midtjylland", "Region Nordjylland"] * 7,
    "Year": [2017, 2017, 2017, 2017, 2017,
             2018, 2018, 2018, 2018, 2018,
             2019, 2019, 2019, 2019, 2019,
             2020, 2020, 2020, 2020, 2020,
             2021, 2021, 2021, 2021, 2021,
             2022, 2022, 2022, 2022, 2022,
             2023, 2023, 2023, 2023, 2023],
    "Stays": [683, 264, 312, 384, 147,
              906, 330, 406, 449, 182,
              1032, 430, 405, 434, 187,
              1100, 445, 447, 443, 179,
              1170, 525, 556, 531, 209,
              1311, 548, 649, 695, 218,
              1394, 582, 715, 706, 220]
}

# Create a DataFrame
shelter_df = pd.DataFrame(shelter_data)

# Replace Danish names with English names for consistency
shelter_df["MappedRegion"] = shelter_df["Region"].map(region_mapping)

# Define Safe[3] hues
safe3_hues = [
    "rgb(229, 245, 224)",  # Light green for low values
    "rgb(161, 217, 155)",  # Mid green
    "rgb(65, 171, 93)",    # Darker green
    "rgb(17, 119, 51)"     # Safe[3] for high values
]

# Calculate the global maximum value for the color scale
max_value = shelter_df["Stays"].max()

# Create the map with dynamic coloring based on "Stays"
fig = px.choropleth_mapbox(
    shelter_df,
    geojson=filtered_geojson,
    locations="MappedRegion",
    featureidkey="properties.name",
    color="Stays",  # Dynamically map stays to the color
    color_continuous_scale=safe3_hues,  # Apply Safe[3] hues
    animation_frame="Year",  # Add the timeline using the 'Year' column
    mapbox_style="carto-positron",
    center={"lat": 56, "lon": 10},  # Approximate center of Denmark
    zoom=5,
    range_color=(0, max_value)  # Fix the range to use the global maximum
)

# Update hovertemplate for all frames
for frame in fig.frames:
    for trace in frame.data:
        trace.update(
            hovertemplate=(
                "<b>Region:</b> %{location}<br>"  
                "<b>Year:</b> %{customdata[1]}<br>"  
                "<b>Stays:</b> %{z}<extra></extra>"  
            )
        )

# Also update traces in the main figure
fig.update_traces(
    customdata=shelter_df[["MappedRegion", "Year"]].to_numpy(),
    hovertemplate=(
        "<b>Region:</b> %{customdata[0]}<br>"  
        "<b>Year:</b> %{customdata[1]}<br>"
        "<b>Stays:</b> %{z}<extra></extra>"    
    )
)

# Update the layout for the title
fig.update_layout(
    title={
        "text": "Stays by Region of Residence and Time",  
        "x": 0.5,  
        "y": 0.95,  # Adjust the vertical position slightly above the plot
        "font": {"size": 20}  
    },
    margin={"r": 0, "t": 100, "l": 0, "b": 0},  
)

# Show the map
fig.show()
