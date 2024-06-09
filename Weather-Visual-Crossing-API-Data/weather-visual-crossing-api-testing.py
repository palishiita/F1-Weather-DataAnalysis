import requests
import pandas as pd
from io import StringIO

# Read the API key
api_key = '577V4NHCBA2A5PJA62QQTTNPF'

# Define the location and date for testing
location = 'Melbourne%20Australia'
date = '2000-03-12'

# Function to fetch weather data for a given location and date
def fetch_weather_data(location, date):
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{date}/{date}'
    params = {
        'unitGroup': 'metric',
        'contentType': 'csv',
        'include': 'days',
        'key': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        print(f"Error fetching data for {location} on {date}: {response.status_code}")
        return pd.DataFrame()

# Fetch and print the weather data
weather_df = fetch_weather_data(location, date)
print(weather_df)