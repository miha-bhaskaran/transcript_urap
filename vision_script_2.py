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

output_folder = 'trans' # CHANGE NAME FOLDER and put pdf name

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
#make this a function that takes in output folder and returns csv files

def vision(output_folder):

    # Directory containing the images
    image_files = glob.glob(os.path.join(output_folder, '*.png'))

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }


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
                            "text": "Extract only course ids and grades earned from the image and output them in CSV format without any additional explanations or text. Capture the course name exactly. Grades are typically A,B,C,D,F, P, NP with +/-. Do not miss any characters. Include special characters"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response_data = response.json()

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


        # Pattern to match CSV files
        #csv_files = glob.glob(os.path.join(output_folder, '*.csv'))
        