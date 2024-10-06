import os
import glob
import pandas as pd

def convert_to_df(file_path):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Check if the required columns exist in the DataFrame
        required_columns_regex = r'^(sub|cour|gr)\w*'

        # Use lower case to match columns case-insensitively
        matching_columns = df.columns[df.columns.str.lower().str.match(required_columns_regex)].tolist()

        print(matching_columns)

        # Check if any required columns are found
        if not matching_columns:
            print(f"Warning: No matching columns found in {file_path}. Dropping this file.")
            return None

        # Keep only the specified columns
        df_filtered = df[matching_columns]
        return df_filtered

    except pd.errors.ParserError as e:
        print(f"Error parsing {file_path}: {e}. Dropping this file.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while processing {file_path}: {e}. Dropping this file.")
        return None

def concatenate_csv_files(output_folder):
    output_file_path = os.path.join(output_folder, output_folder + '_combined.csv')
    
    csv_files = glob.glob(os.path.join(output_folder, '*.csv'))
    print("CSV Files Found:", csv_files)
    
    all_dataframes = []

    for file_path in csv_files:
        df = convert_to_df(file_path)
        if df is not None:
            all_dataframes.append(df)

    if all_dataframes:
        # Concatenate all the DataFrames if there are any valid ones
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        
        # Save the combined DataFrame to a CSV file
        combined_df.to_csv(output_file_path, index=False)
        print(f"All valid CSV files have been combined into: {output_file_path}")
    else:
        print("No valid CSV files to concatenate.")

# Example usage
output_folder = 'herkimer_SUNYawsBoto'  # Replace with your actual output folder path
concatenate_csv_files(output_folder)
