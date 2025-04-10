import pandas as pd

# file b is validation


def match_percentage(file_a, file_b):
    
    def process_line(line):
        for char in ['"', "'", ",", "`"]:
            line = line.replace(char, "")
        return line.strip()

    
    with open(file_a, "r") as f:
        lines_a = set(process_line(line) for line in f)

   
    lines_b = set()
    line_count_b = 0  # Initialize the line counter for file b
    with open(file_b, "r") as f:
        for line in f:
            processed_line = process_line(line)
            lines_b.add(processed_line)
            line_count_b += 1  # Increment the counter for each line read

   
    unmatched_lines_b = lines_b - lines_a

    unmatched_lines_b.discard("CourseGrade")

    
    match_percentage = (1 - len(unmatched_lines_b) / line_count_b) * 100

    if unmatched_lines_b:
        print("\nUnmatched lines from file_b:", "FILE A:", file_a, "FILE B", file_b)
        for line in unmatched_lines_b:
            print(line)

    print("Match percentage: ", match_percentage, "%")
