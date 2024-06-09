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

# Function to divide a DataFrame into three batches based on percentage
def divide_into_batches(df):
    total_rows = len(df)
    batch1_size = int(total_rows * 0.7)  # 70% of rows
    batch2_size = int(total_rows * 0.2)  # 20% of rows
    batch3_size = total_rows - batch1_size - batch2_size  # Remaining 10% of rows

    batch1 = df.iloc[:batch1_size]
    batch2 = df.iloc[batch1_size:batch1_size + batch2_size]
    batch3 = df.iloc[batch1_size + batch2_size:]

    return batch1, batch2, batch3

# Process each CSV file
for file in csv_files:
    file_path = os.path.join(source_folder_path, file)
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Divide the DataFrame into three batches based on percentage
    batch1, batch2, batch3 = divide_into_batches(df)
    
    # Save each batch into the corresponding directory
    batch1.to_csv(os.path.join(batch1_path, file), index=False)
    batch2.to_csv(os.path.join(batch2_path, file), index=False)
    batch3.to_csv(os.path.join(batch3_path, file), index=False)

print(f"Files have been distributed into batches:\nBatch1: {len(os.listdir(batch1_path))} files\nBatch2: {len(os.listdir(batch2_path))} files\nBatch3: {len(os.listdir(batch3_path))} files")