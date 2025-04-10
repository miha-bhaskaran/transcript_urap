import pandas as pd


def read_csv(file_path):
    """Read a CSV file into a pandas DataFrame."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def calculate_match_percentage(file1, file2):
    """Calculate the match percentage between two CSV files."""
    df1 = read_csv(file1)
    df2 = read_csv(file2)

    if df1 is None or df2 is None:
        return None

    # Drop duplicates and sort data to ensure consistent comparison
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    df1 = df1.fillna("").applymap(str.strip)
    df2 = df2.fillna("").applymap(str.strip)

    print(df1)
    print(df2)

    combined = pd.concat([df1, df2], ignore_index=True)
    unique_rows = combined.drop_duplicates(keep=False)
    unique_rows = combined.drop_duplicates(keep=False)
    print(unique_rows)

    # Calculate matching rows (total rows minus unique rows)
    matching_rows = len(combined) - len(unique_rows)
    total_unique_rows = len(pd.concat([df1, df2]).drop_duplicates())

    # Calculate match percentage
    if total_unique_rows == 0:
        return 100.0  # Both files are empty or identical
    match_percentage = (matching_rows / total_unique_rows) * 100

    return match_percentage


# Example usage:
file_path1 = "west_check.csv"
file_path2 = "validation/west_mich_1.csv"
match_pct = calculate_match_percentage(file_path1, file_path2)
print(f"The match percentage between the two files is: {match_pct:.2f}%")
