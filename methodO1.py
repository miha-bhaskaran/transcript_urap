import os
import base64
import requests
import csv

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def extract_tables_with_gpto1(api_key, image_path):
    image_base64 = encode_image_to_base64(image_path)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o",  # OpenAI's GPT-4o
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract all tables from this image and return each table as plain CSV-formatted rows, separated by empty lines."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 4096
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    result = response.json()

    try:
        print("Raw GPT-4o response:")
        print(result)
        text_response = result["choices"][0]["message"]["content"]
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
        print("Error parsing GPT-4o response:", e)
        return []

def save_table_to_csv(table, csv_path):
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in table:
            writer.writerow(row)

def methodO1(folder_path, api_key, output_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            print(f"Processing {filename} with GPT-4o...")

            tables = extract_tables_with_gpto1(api_key, image_path)
            for i, table in enumerate(tables):
                csv_name = f"{os.path.splitext(filename)[0]}_gpto1_table_{i + 1}.csv"
                csv_path = os.path.join(output_path, csv_name)
                save_table_to_csv(table, csv_path)
                print(f"Saved table {i + 1} to {csv_path}")
