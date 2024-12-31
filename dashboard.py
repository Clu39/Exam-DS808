from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import json

# Custom Pie Chart Function
def create_pie_chart():
    data = {
        "Age ": ["18-24 years", "25-29 years", "30-39 years", "40-49 years", "50 years and over", "Age not stated"],
        "Women ": [401, 478, 1051, 626, 336, 138]
    }
    df = pd.DataFrame(data)
    total = df["Women "].sum()
    df["Percentage "] = df["Women "].apply(lambda x: f"{(x / total * 100):.2f}%")
    df["Legend_Label"] = df["Age "]
    custom_colors = {
        "18-24 years": "rgb(136, 34, 85)",
        "25-29 years": "rgb(51, 34, 136)",
        "30-39 years": "rgb(17, 119, 51)",
        "40-49 years": "rgb(136, 204, 238)",
        "50 years and over": "rgb(153, 153, 51)",
        "Age not stated": "rgb(221, 204, 119)"
    }
    fig = px.pie(
        df, names="Legend_Label", values="Women ", title="Age Distribution of Women",
        color="Legend_Label", color_discrete_map=custom_colors, hole=0.5
    )
    fig.update_traces(
        textinfo="none",
        hovertemplate="<b>Age Group:</b> %{label}<br><b>Women:</b> %{value}<br><b>Percentage:</b> %{percent}<extra></extra>"
    )
    fig.update_layout(
        title=dict(text="Age Distribution of Women", x=0.5, font=dict(size=20)),
        annotations=[dict(
            text="Year: 2023", x=0.5, y=0.5, font=dict(size=14, color="gray"),
            showarrow=False, align="center"
        )],
        legend_title=dict(text="Age Group"),
        font=dict(size=12)
    )
    return fig

# Custom Bar Chart Function
def create_bar_chart():
    data = {
        'TID': [2023] * 12,
        'KMDR': ['1 day', '1 day', '2-5 days', '2-5 days', '6-30 days', '6-30 days',
                 '31-119 days', '31-119 days', '120-364 days', '120-364 days', 'All year', 'All year'],
        'BEBOSTAT': ['Women', 'Children', 'Women', 'Children', 'Women', 'Children',
                     'Women', 'Children', 'Women', 'Children', 'Women', 'Children'],
        'INDHOLD': [140, 80, 248, 212, 731, 612, 1093, 1000, 755, 614, 63, 56]
    }
    df = pd.DataFrame(data)
    fig = px.bar(
        df, x='KMDR', y='INDHOLD', color='BEBOSTAT', barmode='group',
        title="Duration of Stays at Women's Shelters",
        labels={'KMDR': 'Duration', 'INDHOLD': 'Stays', 'BEBOSTAT': 'Resident'},
        hover_data={'KMDR': True, 'INDHOLD': True, 'BEBOSTAT': True}
    )

    fig.for_each_trace(
        lambda trace: trace.update(
            customdata=df[df["BEBOSTAT"] == trace.name][["BEBOSTAT"]].to_numpy(),
            hovertemplate=(
                "<b>Resident:</b> %{customdata[0]}<br>"
                "<b>Duration:</b> %{x}<br>"
                "<b>Stays:</b> %{y}<extra></extra>"
            )
        )
    )

    fig.for_each_trace(
        lambda trace: trace.update(marker_color='rgb(136, 204, 238)' if trace.name == 'Women' else 'rgb(17, 119, 51)')
    )
    fig.add_annotation(
        x=0.5, y=1.15, xref="paper", yref="paper", text="Year: 2023",
        showarrow=False, font=dict(size=14, color="gray"), align="center"
    )
    fig.update_layout(
        title=dict(text="Duration of Stays", x=0.5, font=dict(size=20)),
        legend_title=dict(text="Resident Status"), legend=dict(x=0.85, y=1)
    )
    return fig

# Custom Line Chart Function
def create_plot_line_chart():
    data = {
        "BEBOSTAT": ["Stays", "Stays", "Stays", "Stays", "Stays", "Stays", "Stays",
                     "Women", "Women", "Women", "Women", "Women", "Women", "Women",
                     "Children", "Children", "Children", "Children", "Children", "Children", "Children"],
        "TID": [2017, 2018, 2019, 2020, 2021, 2022, 2023,
                2017, 2018, 2019, 2020, 2021, 2022, 2023,
                2017, 2018, 2019, 2020, 2021, 2022, 2023],
        "INDHOLD": [1971, 2421, 2627, 2744, 3117, 3606, 3776,
                    1691, 2046, 2194, 2346, 2619, 2949, 3030,
                    1728, 1931, 1960, 2165, 2273, 2370, 2574]
    }

    df = pd.DataFrame(data)

    fig = px.line(
        df,
        x="TID",
        y="INDHOLD",
        color="BEBOSTAT",
        title="Number of Stays, Women, and Children over Time",
        labels={
            "TID": "Year",
            "INDHOLD": "Number",
            "BEBOSTAT": "Resident Status"
        },
        markers=True,
        color_discrete_map={
            "Stays": "rgb(221, 204, 119)",
            "Women": "rgb(136, 204, 238)",
            "Children": "rgb(17, 119, 51)"
        }
    )

    fig.for_each_trace(lambda trace: trace.update(
        customdata=df[df["BEBOSTAT"] == trace.name][["BEBOSTAT"]].to_numpy(),
        hovertemplate=(
            "<b>Resident Status:</b> %{customdata[0]}<br>"
            "<b>Year:</b> %{x}<br>"
            "<b>Number:</b> %{y}<extra></extra>"
        )
    ))

    fig.update_layout(
        title=dict(
            text="Number of Stays, Women, and Children over Time",
            x=0.5,
            font=dict(size=20)
        ),
        xaxis=dict(
            title="Year",
            tickmode='linear'
        ),
        yaxis=dict(
            title="Number"
        ),
        legend_title=dict(text="Resident Status"),
        font=dict(size=14),
        margin=dict(l=40, r=40, t=80, b=40)
    )

    fig.add_vline(
        x=2020.25,
        line=dict(color="rgb(136, 34, 85)", width=2, dash="dash"),
        annotation_text="Covid-19 Lockdown (Mar.20)",
        annotation_position="top left"
    )
    fig.add_vline(
        x=2021.50,
        line=dict(color="rgb(136, 34, 85)", width=2, dash="dash"),
        annotation_text="Reopening Phase 3 (Jun.21)",
        annotation_position="top left"
    )
    return fig

# Geomap Function
def create_geomap():
    with open("filtered_denmark_regions.geojson", "r") as file:
        filtered_geojson = json.load(file)

    region_mapping = {
        "Region Hovedstaden": "Capital Region of Denmark",
        "Region Sjælland": "Region Zealand",
        "Region Syddanmark": "Region of Southern Denmark",
        "Region Midtjylland": "Central Denmark Region",
        "Region Nordjylland": "North Denmark Region"
    }

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

    shelter_df = pd.DataFrame(shelter_data)
    shelter_df["MappedRegion"] = shelter_df["Region"].map(region_mapping)

    safe3_hues = [
        "rgb(229, 245, 224)",
        "rgb(161, 217, 155)",
        "rgb(65, 171, 93)",
        "rgb(17, 119, 51)"
    ]

    max_value = shelter_df["Stays"].max()

    fig = px.choropleth_mapbox(
        shelter_df,
        geojson=filtered_geojson,
        locations="MappedRegion",
        featureidkey="properties.name",
        color="Stays",
        color_continuous_scale=safe3_hues,
        animation_frame="Year",
        mapbox_style="carto-positron",
        center={"lat": 56, "lon": 10},
        zoom=5,
        range_color=(0, max_value)
    )

    for frame in fig.frames:
        for trace in frame.data:
            trace.update(
                customdata=shelter_df[shelter_df['Year'] == int(frame.name)][["MappedRegion", "Year", "Stays"]].to_numpy(),
                hovertemplate=(
                    "<b>Region:</b> %{customdata[0]}<br>"
                    "<b>Year:</b> %{customdata[1]}<br>"
                    "<b>Stays:</b> %{customdata[2]}<extra></extra>"
                )
            )

    fig.update_traces(
        customdata=shelter_df[["MappedRegion", "Year", "Stays"]].to_numpy(),
        hovertemplate=(
            "<b>Region:</b> %{customdata[0]}<br>"
            "<b>Year:</b> %{customdata[1]}<br>"
            "<b>Stays:</b> %{customdata[2]}<extra></extra>"
        )
    )

    fig.update_layout(
        title={
            "text": "Stays by Region of Residence and Time",
            "x": 0.5,
            "y": 0.95,
            "font": {"size": 20}
        },
        margin={"r": 0, "t": 100, "l": 0, "b": 0},
    )

    return fig

# Initialize the Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div(
    style={
        "font-family": "Arial, sans-serif",
        "padding": "20px",
        "background-color": "#f9f9f9",
    },
    children=[
        html.H1("Interactive Visualisation of Women's Shelters in Denmark", style={"text-align": "center", "margin-bottom": "40px", "color": "#1a3c40"}),
        html.H3("Hacher Al-Badri & Cindy Lu", style={"text-align": "center", "margin-bottom": "5px", "color": "#1a3c40"}),
        html.H5("Data Science (DS808), University of Southern Denmark", style={"text-align": "center", "margin-bottom": "40px", "color": "#1a3c40"}),

        # Metrics Row
        html.Div(
            style={"display": "flex", "justify-content": "center", "gap": "30px", "margin-bottom": "40px"},
            children=[
                html.Div(
                    style={"background-color": "#e0e0e0", "padding": "30px", "border-radius": "8px", "width": "300px"},
                    children=[
                        html.H2("3,030", style={"color": "rgb(17, 119, 51)", "font-size": "36px"}),
                        html.P("Number of women staying at women's shelters", style={"font-size": "16px"}),
                        html.P("2023", style={"font-size": "14px", "color": "#555"}),
                    ],
                ),
                html.Div(
                    style={"background-color": "#e0e0e0", "padding": "30px", "border-radius": "8px", "width": "300px"},
                    children=[
                        html.H2("2,574", style={"color": "rgb(17, 119, 51)", "font-size": "36px"}),
                        html.P("Number of children staying at women's shelters", style={"font-size": "16px"}),
                        html.P("2023", style={"font-size": "14px", "color": "#555"}),
                    ],
                ),
            ],
        ),

        # Line Chart Row
        html.Div(
            style={"margin-bottom": "40px"},
            children=[dcc.Graph(id="line-chart", figure=create_plot_line_chart())],
        ),

        # Charts Row 2: Pie Chart and Bar Chart
        html.Div(
            style={"display": "flex", "justify-content": "space-between", "margin-bottom": "40px"},
            children=[
                html.Div(
                    style={"flex": "1", "margin-right": "20px"},
                    children=[dcc.Graph(id="pie-chart", figure=create_pie_chart())],
                ),
                html.Div(
                    style={"flex": "1", "margin-left": "20px"},
                    children=[dcc.Graph(id="bar-chart", figure=create_bar_chart())],
                ),
            ],
        ),

        # Geomap Row
        html.Div(
            style={"margin-bottom": "40px", "height": "700px"},  # Adjust the height here
            children=[dcc.Graph(id="geomap", figure=create_geomap(), style={"height": "100%"})],
        ),
    ],
)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
