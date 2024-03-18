import pandas as pd

# Load the CSV files into pandas DataFrames
df_a = pd.read_csv('western_mihc_transcript.pdf_20240318000833.csv')
df_b = pd.read_csv('validation/west_mich.csv')

# testing2 is the truth file df_b
#for asu
# df_a['Degree:'] = df_a['Degree:'].astype(str)
# df_b['Degree:'] = df_b['Degree:'].astype(str)
##################

## for edmunds
# df_a['GRADE'] = df_a['GRADE'].astype(str)
# df_b['GRADE'] = df_b['GRADE'].astype(str)

##for taylor
# df_a['Course'] = df_a['Course'].astype(str)
# df_b['Course'] = df_b['Course'].astype(str)

#for uva
# df_a['Beginning of Undergraduate Record'] = df_a['Beginning of Undergraduate Record'].astype(str)
# df_b['Beginning of Undergraduate Record'] =  df_b['Beginning of Undergraduate Record'].astype(str)

#for west_mich
df_a['Degrees Awarded'] = df_a['Degrees Awarded'].astype(str)
df_b['Degrees Awarded'] = df_b['Degrees Awarded'].astype(str)

df_a['Grade:'] = df_a['Grade:'].astype(str)
df_b['Grade:'] = df_b['Grade:'].astype(str)

df_a['Classification:'] = df_a['Classification:'].astype(str)
df_b['Classification:'] = df_b['Classification:'].astype(str)



df_a_unique = df_a.drop_duplicates()
df_b_unique = df_b.drop_duplicates()

# Find the intersection of the two DataFrames without duplicates
intersection_unique = pd.merge(df_b_unique, df_a_unique, how='inner')

# Calculate the percentage of unique information in both DataFrames, from B's perspective
percentage_in_both_unique = (len(intersection_unique) / len(df_b_unique)) * 100
# calculates the true positive rows not each character
print(f"True Positive Percentage: {percentage_in_both_unique}%")
merged_df = pd.merge(df_b_unique, df_a_unique, how='outer', indicator=True)

# Filter rows that are only in the ground truth file (df_b_unique)
rows_not_matched = merged_df[merged_df['_merge'] == 'left_only'].drop('_merge', axis=1)

# Print the rows from df_b_unique that did not match with df_a_unique
print(rows_not_matched)