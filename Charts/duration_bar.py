# Define the function
def create_bar_chart():
    import pandas as pd
    import plotly.express as px

    data = {
        'TID': [2023] * 12,
        'KMDR': ['1 day', '1 day', '2-5 days', '2-5 days', '6-30 days', '6-30 days',
                 '31-119 days', '31-119 days', '120-364 days', '120-364 days', 'All year', 'All year'],
        'BEBOSTAT': ['Women', 'Children', 'Women', 'Children', 'Women', 'Children',
                     'Women', 'Children', 'Women', 'Children', 'Women', 'Children'],
        'INDHOLD': [140, 80, 248, 212, 731, 612, 1093, 1000, 755, 614, 63, 56]
    }
    df = pd.DataFrame(data)

    # Create the bar chart
    fig = px.bar(
        df,
        x='KMDR',
        y='INDHOLD',
        color='BEBOSTAT',
        barmode='group',
        title="Duration of Stays at Women's Shelters",
        labels={
            'KMDR': 'Duration',
            'INDHOLD': 'Stays',
            'BEBOSTAT': 'Resident'
        }
    )

    # Update hovertemplate to use the actual data
    fig.for_each_trace(
        lambda trace: trace.update(
            customdata=df[df["BEBOSTAT"] == trace.name][["BEBOSTAT"]].to_numpy(),
            hovertemplate=(
                "<b>Resident:</b> %{customdata[0]}<br>"  # Use actual Resident data
                "<b>Duration:</b> %{x}<br>"              # Display the duration (e.g., '1 day')
                "<b>Stays:</b> %{y}<extra></extra>"      # Display the stays count
            )
        )
    )

    # Customize colors
    fig.for_each_trace(
        lambda trace: trace.update(marker_color='rgb(136, 204, 238)' if trace.name == 'Women' else 'rgb(17, 119, 51)')
    )

    # Layout updates
    fig.update_layout(
        title=dict(
            text="Duration of Stays at Women's Shelters in Denmark<br><span style='font-size:14px; color:gray;'>Year: 2023</span>",  # Add "Year: 2023" below the title
            x=0.5,
            font=dict(size=20)
        ),
        legend_title=dict(text="Resident Status"),
        legend=dict(x=0.85, y=1)
    )

    # Display the chart
    fig.show()

# Call the function to display the chart
create_bar_chart()
