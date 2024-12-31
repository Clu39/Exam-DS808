import pandas as pd
import os

def clean_data(file_path):
    try:
        # Debug: Check if file exists
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return None
        
        # Read the CSV file with encoding fallback
        print(f"Processing file: {file_path}")
        df = pd.read_csv(file_path, encoding='latin1')
        
        # Skip metadata rows and reset the header
        df_cleaned = df.iloc[2:].reset_index(drop=True)
        
        # Expand delimited strings into separate columns
        df_cleaned = df_cleaned.apply(lambda row: pd.Series(row.iloc[0].split(';')), axis=1)
        
        # Set the first row as header
        df_cleaned.columns = df_cleaned.iloc[0]
        df_cleaned = df_cleaned[1:]  # Drop the header row from the data
        
        # Strip any unnecessary whitespace or quotes
        df_cleaned.columns = df_cleaned.columns.str.strip('" ')
        df_cleaned = df_cleaned.apply(lambda col: col.map(lambda x: x.strip('" ') if isinstance(x, str) else x))
        
        # Reset index to ensure no conflicts
        df_cleaned.reset_index(drop=True, inplace=True)
        
        # Ensure unique column names
        df_cleaned.columns = make_column_names_unique(df_cleaned.columns)
        
        # Rename columns (adjust as per dataset structure)
        df_cleaned.rename(columns={
            'nan_1': 'Unknown', 
            'nan_2': '2017', 
            'nan_3': '2018', 
            'nan_4': '2019',
            'nan_5': '2020',    
            'nan_6': '2021',
            'nan_7': '2022',
            'nan_8': '2023'
         
            
        }, inplace=True)
        
        # Remove duplicate rows
        df_cleaned = df_cleaned.drop_duplicates()
        
        return df_cleaned
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

# Custom function to ensure unique column names
def make_column_names_unique(columns):
    seen = {}
    unique_columns = []
    for col in columns:
        if col in seen:
            seen[col] += 1
            unique_columns.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 0
            unique_columns.append(col)
    return unique_columns

# File paths
age_file = 'Age.csv'
ancestry_file = 'Ancestry.csv'
region_file = 'Region.csv'


# Clean each dataset
age_data_cleaned = clean_data(age_file)
ancestry_data_cleaned = clean_data(ancestry_file)
region_data_cleaned = clean_data(region_file)

# Combine all cleaned datasets into one if they were processed successfully
if age_data_cleaned is not None and ancestry_data_cleaned is not None and region_data_cleaned is not None:
    # Standardize the columns to avoid conflicts
    common_columns = list(set(age_data_cleaned.columns) | set(ancestry_data_cleaned.columns) | set(region_data_cleaned.columns))
    age_data_cleaned = age_data_cleaned.reindex(columns=common_columns, fill_value=None)
    ancestry_data_cleaned = ancestry_data_cleaned.reindex(columns=common_columns, fill_value=None)
    region_data_cleaned = region_data_cleaned.reindex(columns=common_columns, fill_value=None)
    
    # Combine the datasets
    combined_data = pd.concat(
        [age_data_cleaned, ancestry_data_cleaned, region_data_cleaned],
        axis=0,
        ignore_index=True
    )
    
    combined_data = combined_data.drop_duplicates()  # Remove any duplicate rows
    
    # Save the combined cleaned dataset
    combined_data.to_csv('Combined_Cleaned_Data.csv', index=False)
    print("All cleaned datasets have been merged and saved to 'Combined_Cleaned_Data.csv'.")
else:
    print("One or more files could not be processed.")
