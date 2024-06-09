import pandas as pd

# File path to the input CSV file
file_path = r'C:\Users\ishii\Documents\Formula-1-And-Weather-Data-Engineering-Project\Weather-Visual-Crossing-API-Data\Data.csv'
filtered_file_path = r'C:\Users\ishii\Documents\Formula-1-And-Weather-Data-Engineering-Project\Weather-Visual-Crossing-API-Data\New-Data.csv'

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

# Filter out rows with dates older than 1970-01-01
df['date'] = pd.to_datetime(df['date'])
df_filtered = df[df['date'] >= pd.to_datetime('1970-01-01')]

# Save the filtered DataFrame to a new CSV file
df_filtered.to_csv(filtered_file_path, index=False)
print(f"Filtered data saved to {filtered_file_path}")