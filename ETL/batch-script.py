import os
import pandas as pd
import re

# Define paths
source_folder_path = r'C:\Users\ishii\Documents\Formula-1-And-Weather-Data-Engineering-Project\ETL\All-files-Batching'
batch_folder_path = r'C:\Users\ishii\Documents\Formula-1-And-Weather-Data-Engineering-Project\ETL\batches'

# List all CSV files in the source folder
csv_files = [f for f in os.listdir(source_folder_path) if f.endswith('.csv')]

# Create batch directories
batch_paths = {
    'Batch1': os.path.join(batch_folder_path, 'Batch1'),
    'Batch2': os.path.join(batch_folder_path, 'Batch2'),
    'Batch3': os.path.join(batch_folder_path, 'Batch3')
}

for path in batch_paths.values():
    os.makedirs(path, exist_ok=True)

# Function to clean date data
def clean_date(date_str):
    # Remove time part if it exists
    date_str = re.sub(r'\s+.*$', '', date_str)
    # Handle date formats
    if re.match(r'\d{1,2}/\d{1,2}/\d{4}', date_str):  # mm/dd/yyyy or m/d/yyyy
        date = pd.to_datetime(date_str, format='%m/%d/%Y', errors='coerce')
    elif re.match(r'\d{4}-\d{2}-\d{2}', date_str):  # yyyy-mm-dd
        date = pd.to_datetime(date_str, format='%Y-%m-%d', errors='coerce')
    else:
        date = pd.NaT
    return date

# Function to divide DataFrame into batches based on year ranges
def divide_by_date(df, date_column):
    df[date_column] = df[date_column].apply(clean_date)
    print(f"Parsed date data: {df[date_column].head()}")
    
    # Output rows with NaT dates
    nat_rows = df[df[date_column].isna()]
    if not nat_rows.empty:
        print(f"Rows with NaT in {date_column} column:")
        print(nat_rows)
    
    batch1 = df[df[date_column].dt.year <= 2000]
    batch2 = df[(df[date_column].dt.year > 2000) & (df[date_column].dt.year <= 2011)]
    batch3 = df[df[date_column].dt.year > 2011]
    return batch1, batch2, batch3

# Process races.csv
races_file = 'races.csv'
races_file_path = os.path.join(source_folder_path, races_file)
races_df = pd.read_csv(races_file_path)
print(f"Original date data in {races_file}: {races_df['date'].head()}")
batch1_races, batch2_races, batch3_races = divide_by_date(races_df, 'date')

# Save the divided races DataFrames
batch1_races.to_csv(os.path.join(batch_paths['Batch1'], 'races.csv'), index=False)
batch2_races.to_csv(os.path.join(batch_paths['Batch2'], 'races.csv'), index=False)
batch3_races.to_csv(os.path.join(batch_paths['Batch3'], 'races.csv'), index=False)

print(f"Races - Batch1 size: {len(batch1_races)}")
print(f"Races - Batch2 size: {len(batch2_races)}")
print(f"Races - Batch3 size: {len(batch3_races)}")

# Process weather.csv
weather_file = 'weather.csv'
weather_file_path = os.path.join(source_folder_path, weather_file)
if os.path.exists(weather_file_path):
    weather_df = pd.read_csv(weather_file_path)
    print(f"Original date data in {weather_file}: {weather_df['date'].head()}")
    batch1_weather, batch2_weather, batch3_weather = divide_by_date(weather_df, 'date')
    
    # Save the divided weather DataFrames
    batch1_weather.to_csv(os.path.join(batch_paths['Batch1'], 'weather.csv'), index=False)
    batch2_weather.to_csv(os.path.join(batch_paths['Batch2'], 'weather.csv'), index=False)
    batch3_weather.to_csv(os.path.join(batch_paths['Batch3'], 'weather.csv'), index=False)
    
    print(f"Weather - Batch1 size: {len(batch1_weather)}")
    print(f"Weather - Batch2 size: {len(batch2_weather)}")
    print(f"Weather - Batch3 size: {len(batch3_weather)}")

print(f"Files have been distributed into batches:\nBatch1: {len(os.listdir(batch_paths['Batch1']))} files\nBatch2: {len(os.listdir(batch_paths['Batch2']))} files\nBatch3: {len(os.listdir(batch_paths['Batch3']))} files")

# Read the batch files for races and weather
batch1_races = pd.read_csv(os.path.join(batch_paths['Batch1'], 'races.csv'))
batch2_races = pd.read_csv(os.path.join(batch_paths['Batch2'], 'races.csv'))
batch3_races = pd.read_csv(os.path.join(batch_paths['Batch3'], 'races.csv'))

# Function to process relational linking for other datasets
def process_relational_linking(file, df, link_column, link_df1, link_df2, link_df3, link_column_name):
    batch1 = df[df[link_column].isin(link_df1[link_column_name])]
    batch2 = df[df[link_column].isin(link_df2[link_column_name])]
    batch3 = df[df[link_column].isin(link_df3[link_column_name])]
    return batch1, batch2, batch3

# Relational linking for other datasets
for file in csv_files:
    if file not in ['races.csv', 'weather.csv']:
        file_path = os.path.join(source_folder_path, file)
        df = pd.read_csv(file_path)
        if 'circuitId' in df.columns:  # Circuits Table: Handled relationship with Races.
            batch1, batch2, batch3 = process_relational_linking(file, df, 'circuitId', batch1_races, batch2_races, batch3_races, 'circuitId')
        elif 'raceId' in df.columns:  # Handled relationships with Races.
            batch1, batch2, batch3 = process_relational_linking(file, df, 'raceId', batch1_races, batch2_races, batch3_races, 'raceId')
        elif 'constructorId' in df.columns:  # Constructors Table: Handled relationships with Results and ConstructorStandings.
            results_df = pd.read_csv(os.path.join(source_folder_path, 'results.csv'))
            batch1 = df[df['constructorId'].isin(results_df[results_df['raceId'].isin(batch1_races['raceId'])]['constructorId'])]
            batch2 = df[df['constructorId'].isin(results_df[results_df['raceId'].isin(batch2_races['raceId'])]['constructorId'])]
            batch3 = df[df['constructorId'].isin(results_df[results_df['raceId'].isin(batch3_races['raceId'])]['constructorId'])]
        elif 'driverId' in df.columns:  # Drivers Table: Handled relationships with Results, DriverStandings, LapTimes, and PitStops.
            results_df = pd.read_csv(os.path.join(source_folder_path, 'results.csv'))
            batch1 = df[df['driverId'].isin(results_df[results_df['raceId'].isin(batch1_races['raceId'])]['driverId'])]
            batch2 = df[df['driverId'].isin(results_df[results_df['raceId'].isin(batch2_races['raceId'])]['driverId'])]
            batch3 = df[df['driverId'].isin(results_df[results_df['raceId'].isin(batch3_races['raceId'])]['driverId'])]
        elif 'statusId' in df.columns:  # Status Table: Handled relationship with Results.
            results_df = pd.read_csv(os.path.join(source_folder_path, 'results.csv'))
            batch1 = df[df['statusId'].isin(results_df[results_df['raceId'].isin(batch1_races['raceId'])]['statusId'])]
            batch2 = df[df['statusId'].isin(results_df[results_df['raceId'].isin(batch2_races['raceId'])]['statusId'])]
            batch3 = df[df['statusId'].isin(results_df[results_df['raceId'].isin(batch3_races['raceId'])]['statusId'])]
        elif file == 'lap_times.csv':  # LapTimes Table: Handled relationships with Races and Drivers.
            batch1, batch2, batch3 = process_relational_linking(file, df, 'raceId', batch1_races, batch2_races, batch3_races, 'raceId')
            drivers_df = pd.read_csv(os.path.join(source_folder_path, 'drivers.csv'))
            batch1 = batch1[batch1['driverId'].isin(drivers_df['driverId'])]
            batch2 = batch2[batch2['driverId'].isin(drivers_df['driverId'])]
            batch3 = batch3[batch3['driverId'].isin(drivers_df['driverId'])]
        elif file == 'pit_stops.csv':  # PitStops Table: Handled relationships with Races and Drivers.
            batch1, batch2, batch3 = process_relational_linking(file, df, 'raceId', batch1_races, batch2_races, batch3_races, 'raceId')
            drivers_df = pd.read_csv(os.path.join(source_folder_path, 'drivers.csv'))
            batch1 = batch1[batch1['driverId'].isin(drivers_df['driverId'])]
            batch2 = batch2[batch2['driverId'].isin(drivers_df['driverId'])]
            batch3 = batch3[batch3['driverId'].isin(drivers_df['driverId'])]
        elif file == 'driver_standings.csv':  # DriverStandings Table: Handled relationships with Races and Drivers.
            batch1, batch2, batch3 = process_relational_linking(file, df, 'raceId', batch1_races, batch2_races, batch3_races, 'raceId')
            drivers_df = pd.read_csv(os.path.join(source_folder_path, 'drivers.csv'))
            batch1 = batch1[batch1['driverId'].isin(drivers_df['driverId'])]
            batch2 = batch2[batch2['driverId'].isin(drivers_df['driverId'])]
            batch3 = batch3[batch3['driverId'].isin(drivers_df['driverId'])]
        elif file == 'constructor_standings.csv':  # ConstructorStandings Table: Handled relationships with Races and Constructors.
            batch1, batch2, batch3 = process_relational_linking(file, df, 'raceId', batch1_races, batch2_races, batch3_races, 'raceId')
            constructors_df = pd.read_csv(os.path.join(source_folder_path, 'constructors.csv'))
            batch1 = batch1[batch1['constructorId'].isin(constructors_df['constructorId'])]
            batch2 = batch2[batch2['constructorId'].isin(constructors_df['constructorId'])]
            batch3 = batch3[batch3['constructorId'].isin(constructors_df['constructorId'])]
        else:
            continue

        batch1.to_csv(os.path.join(batch_paths['Batch1'], file), index=False)
        batch2.to_csv(os.path.join(batch_paths['Batch2'], file), index=False)
        batch3.to_csv(os.path.join(batch_paths['Batch3'], file), index=False)
        print(f"Processed relational file: {file}")
        print(f"Batch1 size: {len(batch1)}")
        print(f"Batch2 size: {len(batch2)}")
        print(f"Batch3 size: {len(batch3)}")

print(f"Files have been distributed into batches:\nBatch1: {len(os.listdir(batch_paths['Batch1']))} files\nBatch2: {len(os.listdir(batch_paths['Batch2']))} files\nBatch3: {len(os.listdir(batch_paths['Batch3']))} files")