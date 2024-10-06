import pandas as pd

def convert_to_df(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Check if the required columns exist in the DataFrame
    required_columns = ['Subject', 'Course', 'Grade']
    for col in required_columns:
        if col not in df.columns:
            print(f"Warning: Column '{col}' not found in {file_path}. Dropping this file.")
            return None

    # Keep only the specified columns
    df_filtered = df[required_columns]

    return df_filtered

# Example usage
file_path = 'herkimer_SUNYawsBoto/page-1_table_4.csv'  # Replace with your actual file path
df_result = convert_to_df(file_path)

if df_result is not None:
    print(df_result.head())  # Display the first few rows of the DataFrame
