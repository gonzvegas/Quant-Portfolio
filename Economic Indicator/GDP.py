import requests
import pandas as pd

# Your FRED API Key
FRED_API_KEY = 'fa390c8cc0db2044b1621ddbf2d9db1d'

# Example Series ID for GDP Growth Rate
series_id = 'A191RL1Q225SBEA'  # This is the ID for the real GDP growth rate

# API URL with parameters
url = f'https://api.stlouisfed.org/fred/series/observations'
params = {
    'series_id': series_id,
    'api_key': FRED_API_KEY,
    'file_type': 'json',
    'observation_start': '2000-01-01',  # Start date for the data
    'observation_end': '2024-01-01',    # End date for the data
    'units': 'lin',                     # No transformation
    'frequency': 'q',                   # Quarterly data
    'aggregation_method': 'avg'         # Average if aggregation is needed
}

# Make the API request
response = requests.get(url, params=params)
data = response.json()

# Convert to DataFrame
observations = data['observations']
df = pd.DataFrame(observations)

# Clean and format the data
df['date'] = pd.to_datetime(df['date'])
df['value'] = pd.to_numeric(df['value'])

# Display the first few rows of the DataFrame
import plotly.express as px

# Create a line chart for GDP Growth Rate
fig = px.line(df, x='date', y='value', title='GDP Growth Rate Over Time')

# Customize the chart
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='GDP Growth Rate (%)',
    hovermode='x unified',
    template='plotly_dark',  # Optional: Use a dark theme for the chart
    xaxis=dict(
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

# Show the plot
fig.write_html("gdp_growth_rate.html")



