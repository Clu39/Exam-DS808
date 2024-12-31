def create_plot_line_chart():
    import pandas as pd
    import plotly.express as px

    # Data from the table, including the new "Children" data
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

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Create a line chart
    fig = px.line(
        df,
        x="TID",
        y="INDHOLD",
        color="BEBOSTAT",
        title="Stays, Women, and Children at Women's Shelters Over Time",
        labels={
            "TID": "Year",
            "INDHOLD": "Number",
            "BEBOSTAT": "Resident Status"
        },
        markers=True,
        color_discrete_map={
            "Total": "rgb(153, 153, 51)",  # Custom color for "Total"
            "Women": "rgb(136, 204, 238)",   # Custom color for "Women"
            "Children": "rgb(17, 119, 51)"  # Custom color for "Children"
        }
    )

    # Ensure customdata is grouped properly for each trace
    fig.for_each_trace(lambda trace: trace.update(
        customdata=df[df["BEBOSTAT"] == trace.name][["BEBOSTAT"]].to_numpy(),  # Group by trace name
        hovertemplate=(
            "<b>Resident Status:</b> %{customdata[0]}<br>"  # Use customdata[0] for BEBOSTAT
            "<b>Year:</b> %{x}<br>"                       # Format the year
            "<b>Number:</b> %{y}<extra></extra>"          # Format the number
        )
    ))

    # Customize the layout for better alignment with the inspiration image
    fig.update_layout(
        title=dict(
            text="Stays, Women, and Children at Women's Shelters Over Time",
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

    # Add vertical line for Denmark's lockdown announcement in March 2020
    fig.add_vline(
        x=2020.25,  # Position adjusted for March 2020
        line=dict(color="rgb(136, 34, 85)", width=2, dash="dash"),
        annotation_text="Covid-19 Lockdown (Mar.20)",
        annotation_position="top left"
    )
    fig.add_vline(
        x=2021.50,  # Position adjusted for June 2021
        line=dict(color="rgb(136, 34, 85)", width=2, dash="dash"),
        annotation_text="Reopening Phase 3 (Jun.21)",
        annotation_position="top left"
    )

    # Display the chart
    fig.show()

# Call the function to create the chart
create_plot_line_chart()
