import time
import requests
import pandas as pd
from io import StringIO

# Read the API key
api_key = '577V4NHCBA2A5PJA62QQTTNPF'

# File path to the input CSV file
file_path = r'C:\Users\ishii\Documents\Formula-1-And-Weather-Data-Engineering-Project\Weather-Visual-Crossing-API-Data\Data.csv'

# Load the CSV file
try:
    df = pd.read_csv(file_path)
    print("Column names in the CSV file:", df.columns.tolist())
except FileNotFoundError:
    print(f"Error: The file at {file_path} was not found.")
    exit(1)
except pd.errors.EmptyDataError:
    print(f"Error: The file at {file_path} is empty.")
    exit(1)

# Define the columns to keep
weather_columns = [
    'tempmax', 'tempmin', 'temp', 'feelslikemax', 'feelslikemin', 'feelslike',
    'dew', 'humidity', 'precip', 'precipprob', 'precipcover', 'preciptype',
    'snow', 'snowdepth', 'windgust', 'windspeed', 'winddir', 'sealevelpressure',
    'cloudcover', 'visibility', 'solarradiation', 'solarenergy', 'uvindex',
    'severerisk', 'conditions', 'description', 'icon', 'stations'
]

# Filter out rows with dates older than 1970-01-01
df['date'] = pd.to_datetime(df['date'])
df = df[df['date'] >= pd.to_datetime('1970-01-01')]

# Initialize an empty DataFrame to store the weather data
weather_data = pd.DataFrame(columns=weather_columns)

# Function to fetch weather data for a given location and date
def fetch_weather_data(location, date):
    formatted_date = date.strftime('%Y-%m-%d')
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{formatted_date}/{formatted_date}'
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
        print(f"Error fetching data for {location} on {formatted_date}: {response.status_code}")
        return pd.DataFrame(columns=weather_columns)

# Iterate over each row in the DataFrame to fetch and append weather data
for index, row in df.iterrows():
    location = row['locationModified']
    date = row['date']
    weather_df = fetch_weather_data(location, date)
    if not weather_df.empty and weather_df.notna().any().any():
        weather_data = pd.concat([weather_data, weather_df[weather_columns]], ignore_index=True)
    time.sleep(1)  # Sleep to avoid hitting API rate limits

# Concatenate the original DataFrame with the weather data if the columns are not already present
if not all(col in df.columns for col in weather_columns):
    df = pd.concat([df.reset_index(drop=True), weather_data.reset_index(drop=True)], axis=1)

# Save the updated DataFrame to a new CSV file
output_file_path = r'C:\Users\ishii\Documents\Formula-1-And-Weather-Data-Engineering-Project\Weather-Visual-Crossing-API-Data\Weather-Data.csv'
df.to_csv(output_file_path, index=False)

print(f"Updated data saved to {output_file_path}")