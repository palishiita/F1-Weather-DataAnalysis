import time
import requests
import pandas as pd
from io import StringIO

# Read the API key
api_key = 'SEPZQXTCDC9BPRVCNAGVATCS9'

# File path to the CSV file
file_path = r'C:\Users\ishii\Documents\Formula-1-And-Weather-Data-Engineering-Project\Weather-Visual-Crossing-API-Data\New-Data.csv'

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

# Define the weather columns to keep
weather_columns = [
    'tempmax', 'tempmin', 'temp', 'feelslikemax', 'feelslikemin', 'feelslike',
    'dew', 'humidity', 'precip', 'precipprob', 'precipcover', 'preciptype',
    'snow', 'snowdepth', 'windgust', 'windspeed', 'winddir', 'sealevelpressure',
    'cloudcover', 'visibility', 'solarradiation', 'solarenergy', 'uvindex',
    'severerisk', 'conditions', 'description', 'icon', 'stations'
]

# Add the weather columns to the DataFrame with default NaN values
for column in weather_columns:
    if column not in df.columns:
        df[column] = pd.NA

# Function to fetch weather data for a given location and date with retries
def fetch_weather_data(location, date):
    formatted_date = date.strftime('%Y-%m-%d')
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{formatted_date}/{formatted_date}'
    params = {
        'unitGroup': 'metric',
        'contentType': 'csv',
        'include': 'days',
        'key': api_key
    }

    retries = 5
    for i in range(retries):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return pd.read_csv(StringIO(response.text))
        elif response.status_code == 429:
            # Exponential backoff with a maximum of 32 seconds
            sleep_time = min(2 ** i, 32)
            print(f"Rate limit hit. Retrying in {sleep_time} seconds...")
            time.sleep(sleep_time)
        else:
            print(f"Error fetching data for {location} on {formatted_date}: {response.status_code}")
            return pd.DataFrame(columns=weather_columns)
    return pd.DataFrame(columns=weather_columns)

# Iterate over each row in the DataFrame to fetch and update weather data
for index, row in df.iterrows():
    location = row['locationModified'].replace('%20', ' ')
    date = pd.to_datetime(row['date']).date()
    weather_df = fetch_weather_data(location, date)
    if not weather_df.empty and weather_df.notna().any().any():
        for column in weather_columns:
            if column in weather_df.columns:
                df.at[index, column] = weather_df[column].iloc[0]
    time.sleep(1)  # Constant delay to avoid hitting API rate limits

# Save the updated DataFrame back to the same CSV file
df.to_csv(file_path, index=False)

print(f"Weather data fetched and updated to {file_path}")