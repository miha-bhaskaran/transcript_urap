import os
import base64
import requests
import csv
import glob, sys, fitz
import pandas as pd


# OpenAI API Key
api_key = "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"  # Replace with your actual API key

# To get better resolution
zoom_x = 2.0  # horizontal zoom
zoom_y = 2.0  # vertical zoom
mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension

output_folder = "trans"  # CHANGE NAME FOLDER and put pdf name
valid = "transcript_1.csv"  # CHANGE

all_files = glob.glob(output_folder + "*.pdf")

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

for filename in all_files:
    doc = fitz.open(filename)  # open document
    for page in doc:  # iterate through the pages
        pix = page.get_pixmap(matrix=mat)  # render page to an image
        output_path = os.path.join(output_folder, f"page-{page.number}.png")
        pix.save(output_path)

# finished converting from pdf to png


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Directory containing the images
image_files = glob.glob(os.path.join(output_folder, "*.png"))

headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

for image_path in image_files:
    # Getting the base64 string
    base64_image = encode_image(image_path)

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract only course ids and grades earned from the image and output them in CSV format without any additional explanations or text. Capture the course name exactly. Grades are typically A,B,C,D,F, P, NP with +/-. Do not miss any characters. Include special characters",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )
    response_data = response.json()

    csv_content = response_data["choices"][0]["message"]["content"]
    csv_lines = csv_content.split("\n")
    csv_data = [line.split(", ") for line in csv_lines if line.strip()]

    # Creating CSV file name based on image file name
    csv_file_name = os.path.splitext(os.path.basename(image_path))[0] + ".csv"
    csv_file_path = os.path.join(output_folder, csv_file_name)

    # Writing the data to a CSV file
    with open(csv_file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)

    print(f"CSV file '{csv_file_path}' has been created and populated.")

# finished creating a folder and generated csv files for each png


# Directory containing the CSV and PNG files output_folder should be the name

# Pattern to match CSV files
csv_files = glob.glob(os.path.join(output_folder, "*.csv"))

# List to hold dataframes
dataframes = []

for file in csv_files:
    # Read each CSV file
    df = pd.read_csv(file)
    # Append the dataframe to the list
    dataframes.append(df)

# Concatenate all dataframes, preserving all columns
combined_df = pd.concat(dataframes, ignore_index=True, sort=False)

# Save the concatenated dataframe to a new CSV file
output_file = os.path.join(output_folder, output_folder + "_total.csv")
combined_df.to_csv(output_file, index=False)

print(f"Combined CSV created at: {output_file}")

# created a combined csv

# find matching percent


def find_matching_lines(file_a, file_b):
    # Function to strip whitespace and quotes from each line
    def process_line(line):
        line = line.lower()
        # Remove all instances of each character from anywhere in the string
        for char in ['"', "'", ",", " ", "`", "csv", "plain", "text"]:
            line = line.replace(char, "")
        return line

    # Read all lines from the first file, processing each one
    with open(file_a, "r") as f:
        lines_a = set(process_line(line) for line in f)

    # Read all lines from the second file, processing each one and count them
    lines_b = set()
    line_count_b = 0  # Initialize the line counter for file b
    with open(file_b, "r") as f:
        for line in f:
            processed_line = process_line(line)
            lines_b.add(processed_line)
            line_count_b += 1  # Increment the counter for each line read

    # Find intersection of both sets to get matching lines
    matching_lines = lines_a.intersection(lines_b)

    non_matching_lines = lines_a - lines_b

    # Print non-matching lines
    print("Non-matching lines in file A:")
    for line in non_matching_lines:
        print(line)

    print("Match percentage: ", len(matching_lines) / line_count_b * 100, "%")


find_matching_lines(
    output_folder + "/" + output_folder + "_total.csv", "validation/" + valid
)
