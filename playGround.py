import pandas as pd


# def find_matching_lines(file_a, file_b):

#      # CHANGE NAME FOLDER and put pdf name
#     # Function to strip whitespace and quotes from each line
#     def process_line(line):
#         #line = line.lower()
#         # Remove all instances of each character from anywhere in the string
#         for char in ['"', "'", ",", " ", "`", "csv", "plain", "text"]:
#             line = line.replace(char, '')
#         return line

#     # Read all lines from the first file, processing each one
#     with open(file_a, 'r') as f:
#         lines_a = set(process_line(line) for line in f)

#     # Read all lines from the second file, processing each one and count them
#     lines_b = set()
#     line_count_b = 0  # Initialize the line counter for file b
#     with open(file_b, 'r') as f:
#         for line in f:
#             processed_line = process_line(line)
#             lines_b.add(processed_line)
#             line_count_b += 1  # Increment the counter for each line read

#     # Find intersection of both sets to get matching lines
#     matching_lines = lines_a.intersection(lines_b)

#     non_matching_lines = lines_a - lines_b

#     # Print non-matching lines
#     print("Non-matching lines in file A:")
#     for line in non_matching_lines:
#         print(line)

 

#     print("Match percentage: ",len(matching_lines)/line_count_b * 100, "%")


    


# find_matching_lines('trans/trans_combined.csv',  'validation/transcript.csv')




# Load the CSV file
df = pd.read_csv('validation/transcript.csv')

# Drop the column
# Replace 'column_name_to_drop' with the name of the column you want to remove
df = df.drop(columns=['Un.'])

# Save the modified DataFrame back to a new CSV file
df.to_csv('validation/transcript1.csv', index=False)

print("Column dropped and new CSV file saved.")
