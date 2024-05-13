import pandas as pd

def calculate_match_percentage(file_a_path, file_b_path):
    # Load CSV files
    df_a = pd.read_csv(file_a_path)
    df_b = pd.read_csv(file_b_path)

    # Remove whitespace from all string entries
    df_a = df_a.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df_b = df_b.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # Drop duplicates if necessary
    df_a_unique = df_a.drop_duplicates()
    df_b_unique = df_b.drop_duplicates()

    # Find the intersection of the two DataFrames
    merged_df = pd.merge(df_a_unique, df_b_unique, how='inner')
    # merged_df_dup = merged_df.drop_duplicates()
    print(df_a_unique)
    print("BROTHER")
    print(merged_df)

    # Calculate the percentage of entries in File A that match with File B
    if len(df_a_unique) > 0:  # Ensure division by zero is not possible
        # match_percentage = 1-(len(merged_df) / len(df_a_unique)) * 100
        match_percentage = ( len(merged_df)) / len(df_a_unique) * 100
    else:
        match_percentage = 0  # If df_a_unique is empty, set match percentage to 0

    return match_percentage

# Define file paths
file_a_path = 'trans_check.csv'  # Replace with the actual path to your file
file_b_path = 'validation/transcript_1.csv'  # Replace with the actual path to your file

# Calculate the match percentage
percentage = calculate_match_percentage(file_a_path, file_b_path)
print(f"True Positive Percentage: {percentage:.2f}%")
