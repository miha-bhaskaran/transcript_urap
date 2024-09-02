import pandas as pd

# file b is validation

def match_percentage(file_a, file_b):
    # Function to strip whitespace and quotes from each line
    def process_line(line):
        for char in ['"', "'", " ", ',', "`"]:
            line = line.replace(char, '')
        return line

    # Read all lines from the first file, processing each one
    with open(file_a, 'r') as f:
        lines_a = set(process_line(line) for line in f)

    # Read all lines from the second file, processing each one and count them
    lines_b = set()
    line_count_b = 0  # Initialize the line counter for file b
    with open(file_b, 'r') as f:
        for line in f:
            processed_line = process_line(line)
            lines_b.add(processed_line)
            line_count_b += 1  # Increment the counter for each line read

    # Find lines in file_b that are not in file_a
    unmatched_lines_b = lines_b - lines_a

    # Calculate the match percentage
    match_percentage = (1 - len(unmatched_lines_b) / line_count_b) * 100

    print("Match percentage: ", match_percentage, "%")
