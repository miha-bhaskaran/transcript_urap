import os
import base64
import requests
import csv
from PIL import Image

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def extract_tables_with_claude(api_key, image_path):
    image_base64 = encode_image_to_base64(image_path)

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    data = {
        "model": "claude-3-sonnet-20240229",  # Sonnet model
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract all tables from this image and return each as rows in CSV format. Only return plain CSV-formatted text."
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_base64
                        }
                    }
                ]
            }
        ],
        "max_tokens": 4096,
        "temperature": 0.2
    }

    response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)
    result = response.json()

    try:
        text_response = result["content"][0]["text"]
        tables = []
        current_table = []
        for line in text_response.strip().splitlines():
            if line.strip() == "":
                if current_table:
                    tables.append(current_table)
                    current_table = []
            else:
                row = [cell.strip() for cell in line.strip().split(",")]
                current_table.append(row)
        if current_table:
            tables.append(current_table)
        return tables
    except Exception as e:
        print("Error parsing Claude response:", e)
        return []

def save_table_to_csv(table, csv_path):
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in table:
            writer.writerow(row)

def methodClaude(folder_path, api_key, output_path):
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            print(f"Processing {filename} with Claude Sonnet...")

            tables = extract_tables_with_claude(api_key, image_path)
            for i, table in enumerate(tables):
                csv_name = f"{os.path.splitext(filename)[0]}_claude_table_{i + 1}.csv"
                csv_path = os.path.join(output_path, csv_name)
                save_table_to_csv(table, csv_path)
                print(f"Saved table {i + 1} to {csv_path}")
