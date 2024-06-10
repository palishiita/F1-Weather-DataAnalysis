import pandas as pd

# Define the path to the races.csv file and the output file for date errors
races_file_path = r'C:\Users\ishii\Documents\Formula-1-And-Weather-Data-Engineering-Project\ETL\All-files-Batching\races.csv'
output_file_path = r'C:\Users\ishii\Documents\Formula-1-And-Weather-Data-Engineering-Project\ETL\date-error.csv'

# Read the races.csv file
races_df = pd.read_csv(races_file_path)

# Check for rows where the date conversion fails
print("\nRows with date parsing issues:")
races_df['date_parsed'] = pd.to_datetime(races_df['date'], format='%d/%m/%Y', errors='coerce')
invalid_dates = races_df[races_df['date_parsed'].isna()]

# Print rows with invalid dates
print(invalid_dates[['date']])

# Save the rows with date parsing issues to a CSV file
invalid_dates.to_csv(output_file_path, index=False)

# Print unique date formats to understand the variations
print("\nUnique date formats in the date column:")
unique_dates = races_df['date'].apply(lambda x: x.split()[-1] if ' ' in x else x).unique()
for date in unique_dates:
    print(date)

print(f"\nRows with date parsing issues have been saved to {output_file_path}")