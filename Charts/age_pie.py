def create_pie_chart():
    import pandas as pd
    import plotly.express as px

    # Data from the table
    data = {
        "Age ": ["18-24 years", "25-29 years", "30-39 years", "40-49 years", "50 years and over", "Age not stated"],
        "Women ": [401, 478, 1051, 626, 336, 138]
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Calculate percentages for the hover info
    total = df["Women "].sum()
    df["Percentage "] = df["Women "].apply(lambda x: f"{(x / total * 100):.2f}%")

    # Use only the age group in the legend label
    df["Legend_Label"] = df["Age "]  # Keep only the age group in the legend

    # Customize colors for the chart
    custom_colors = {
        "18-24 years": "rgb(136, 34, 85)",
        "25-29 years": "rgb(51, 34, 136)",
        "30-39 years": "rgb(17, 119, 51)",
        "40-49 years": "rgb(136, 204, 238)",
        "50 years and over": "rgb(153, 153, 51)",
        "Age not stated": "rgb(221, 204, 119)"
    }

    # Create a pie chart
    fig = px.pie(
        df,
        names="Legend_Label",  # Use labels without percentages for the legend
        values="Women ",
        title="Age Distribution of Women in Women's Shelters.",
        color="Legend_Label",  # Map the color to the age groups
        color_discrete_map=custom_colors,  # Use the custom color map
        hole=0.5  # Donut-style chart
    )

    # Update trace to include hover info and remove slice labels
    fig.update_traces(
        textinfo="none",  # Remove all labels from the slices
        hovertemplate="<b>Age Group:</b> %{label}<br><b>Women:</b> %{value}<br><b>Percentage:</b> %{percent}<extra></extra>"
    )

    # Customize layout for the title and subtitle
    fig.update_layout(
        title=dict(
            text="Age Distribution of Women in Women's Shelters.",
            x=0.5,
            font=dict(size=20)
        ),
        annotations=[
            dict(
                text="Year: 2023",
                x=0.5,
                y=0.5,
                font=dict(size=14, color="gray"),
                showarrow=False,
                align="center"
            )
        ],
        legend_title=dict(text="Age Group"),
        font=dict(size=12)
    )

    # Display the chart
    fig.show()
