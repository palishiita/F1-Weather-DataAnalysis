import os
import pandas as pd

# Define paths
source_folder_path = r'C:\Users\ishii\Documents\Formula-1-And-Weather-Data-Engineering-Project\ETL\All-files-Batching'
batch_folder_path = r'C:\Users\ishii\Documents\Formula-1-And-Weather-Data-Engineering-Project\ETL\batches'

# List all CSV files in the source folder
csv_files = [f for f in os.listdir(source_folder_path) if f.endswith('.csv')]

# Create batch directories
batch1_path = os.path.join(batch_folder_path, 'Batch1')
batch2_path = os.path.join(batch_folder_path, 'Batch2')
batch3_path = os.path.join(batch_folder_path, 'Batch3')

os.makedirs(batch1_path, exist_ok=True)
os.makedirs(batch2_path, exist_ok=True)
os.makedirs(batch3_path, exist_ok=True)

# Function to divide DataFrame into batches based on year ranges
def divide_by_date(df, date_column):
    df[date_column] = pd.to_datetime(df[date_column])
    batch1 = df[df[date_column].dt.year <= 2000]
    batch2 = df[(df[date_column].dt.year > 2000) & (df[date_column].dt.year <= 2011)]
    batch3 = df[df[date_column].dt.year > 2011]
    return batch1, batch2, batch3

# Dictionary to hold DataFrames for relational linking
dataframes = {}

# Process each CSV file
for file in csv_files:
    file_path = os.path.join(source_folder_path, file)
    df = pd.read_csv(file_path)
    
    if 'date' in df.columns:
        batch1, batch2, batch3 = divide_by_date(df, 'date')
        batch1.to_csv(os.path.join(batch1_path, file), index=False)
        batch2.to_csv(os.path.join(batch2_path, file), index=False)
        batch3.to_csv(os.path.join(batch3_path, file), index=False)
    else:
        dataframes[file] = df

# Use the races DataFrame to divide the rest of the datasets
races_df = pd.read_csv(os.path.join(source_folder_path, 'races.csv'))
batch1_races, batch2_races, batch3_races = divide_by_date(races_df, 'date')

# Save the divided races DataFrames
batch1_races.to_csv(os.path.join(batch1_path, 'races.csv'), index=False)
batch2_races.to_csv(os.path.join(batch2_path, 'races.csv'), index=False)
batch3_races.to_csv(os.path.join(batch3_path, 'races.csv'), index=False)

# Process the weather-data CSV
weather_data_path = os.path.join(source_folder_path, 'weather-data.csv')
if os.path.exists(weather_data_path):
    weather_df = pd.read_csv(weather_data_path)
    batch1_weather, batch2_weather, batch3_weather = divide_by_date(weather_df, 'date')
    batch1_weather.to_csv(os.path.join(batch1_path, 'weather-data.csv'), index=False)
    batch2_weather.to_csv(os.path.join(batch2_path, 'weather-data.csv'), index=False)
    batch3_weather.to_csv(os.path.join(batch3_path, 'weather-data.csv'), index=False)

# Relational linking for other datasets
for file, df in dataframes.items():
    if 'circuitId' in df.columns:
        batch1 = df[df['circuitId'].isin(batch1_races['circuitId'])]
        batch2 = df[df['circuitId'].isin(batch2_races['circuitId'])]
        batch3 = df[df['circuitId'].isin(batch3_races['circuitId'])]
    elif 'raceId' in df.columns:
        batch1 = df[df['raceId'].isin(batch1_races['raceId'])]
        batch2 = df[df['raceId'].isin(batch2_races['raceId'])]
        batch3 = df[df['raceId'].isin(batch3_races['raceId'])]
    elif 'constructorId' in df.columns:
        results_df = dataframes.get('results.csv')
        batch1 = df[df['constructorId'].isin(results_df[results_df['raceId'].isin(batch1_races['raceId'])]['constructorId'])]
        batch2 = df[df['constructorId'].isin(results_df[results_df['raceId'].isin(batch2_races['raceId'])]['constructorId'])]
        batch3 = df[df['constructorId'].isin(results_df[results_df['raceId'].isin(batch3_races['raceId'])]['constructorId'])]
    elif 'driverId' in df.columns:
        results_df = dataframes.get('results.csv')
        batch1 = df[df['driverId'].isin(results_df[results_df['raceId'].isin(batch1_races['raceId'])]['driverId'])]
        batch2 = df[df['driverId'].isin(results_df[results_df['raceId'].isin(batch2_races['raceId'])]['driverId'])]
        batch3 = df[df['driverId'].isin(results_df[results_df['raceId'].isin(batch3_races['raceId'])]['driverId'])]
    elif 'statusId' in df.columns:
        results_df = dataframes.get('results.csv')
        batch1 = df[df['statusId'].isin(results_df[results_df['raceId'].isin(batch1_races['raceId'])]['statusId'])]
        batch2 = df[df['statusId'].isin(results_df[results_df['raceId'].isin(batch2_races['raceId'])]['statusId'])]
        batch3 = df[df['statusId'].isin(results_df[results_df['raceId'].isin(batch3_races['raceId'])]['statusId'])]
    else:
        continue

    batch1.to_csv(os.path.join(batch1_path, file), index=False)
    batch2.to_csv(os.path.join(batch2_path, file), index=False)
    batch3.to_csv(os.path.join(batch3_path, file), index=False)

print(f"Files have been distributed into batches:\nBatch1: {len(os.listdir(batch1_path))} files\nBatch2: {len(os.listdir(batch2_path))} files\nBatch3: {len(os.listdir(batch3_path))} files")