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