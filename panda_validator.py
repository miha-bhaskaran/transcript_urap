import pandas as pd

# Load the CSV files into pandas DataFrames
df_a = pd.read_csv('path_to_file_a.csv')
df_b = pd.read_csv('path_to_file_b.csv')

# Assuming you want to compare all columns, ensure they have the same columns for a fair comparison
# This step may vary depending on your specific need for comparison
df_a = df_a[df_b.columns]

# Find the intersection of the two DataFrames
intersection = pd.merge(df_b, df_a, how='inner')

# Calculate the percentage
percentage_in_both = (len(intersection) / len(df_b)) * 100

print(f"Percentage of information in both File A and File B, from B's perspective: {percentage_in_both}%")
