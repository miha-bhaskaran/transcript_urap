import os
import base64
import requests
import csv
import glob
import fitz
import pandas as pd
from prompts import OPENAI_API_KEY, SYSTEM_PROMPT, get_user_prompt, USER_PROMPT_EXAMPLE

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to read the example CSV file
def read_example_csv(csv_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        return [row for row in reader]

# Main function that takes an example image and example CSV for one-shot learning
def method_vision_osl(output_folder, example_image_path, example_csv_path):
    # Read the example CSV file
    example_csv_data = read_example_csv(example_csv_path)
    example_csv_text = "\n".join([", ".join(row) for row in example_csv_data])

    # Encode the example image
    example_image_base64 = encode_image(example_image_path)

    # Directory containing the images
    image_files = glob.glob(os.path.join(output_folder, '*.png'))

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    for image_path in image_files:
        # Getting the base64 string
        base64_image = encode_image(image_path)

        payload = {
            "model": "gpt-4o-2024-05-13",
            "messages": [
               SYSTEM_PROMPT,
                {
                    "role": "user",
                    "content": USER_PROMPT_EXAMPLE.format(example_csv_text=example_csv_text)
                },
                {
                    "role": "user",
                    "content": "Below is the example image:",
                    "name": "example_image",
                    "type": "image",
                    "image_url": f"data:image/jpeg;base64,{example_image_base64}"
                },
                {
                    "role": "user",
                    "content": "Below is the image to process:",
                    "name": "process_image",
                    "type": "image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}"
                }
            ],
            "max_tokens": 400
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        
        try:
            response_data = response.json()
        except ValueError:
            print(f"Error: Unable to decode JSON response for image {image_path}")
            print(response.text)
            continue

        if 'choices' not in response_data:
            print(f"Error: 'choices' not in response for image {image_path}")
            print(response_data)
            continue

        csv_content = response_data['choices'][0]['message']['content']
        csv_lines = csv_content.split("\n")
        csv_data = [line.split(", ") for line in csv_lines if line.strip()]

        # Creating CSV file name based on image file name
        csv_file_name = os.path.splitext(os.path.basename(image_path))[0] + '.csv'
        csv_file_path = os.path.join(output_folder, csv_file_name)

        # Writing the data to a CSV file
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(csv_data)

        print(f"CSV file '{csv_file_path}' has been created and populated.")
