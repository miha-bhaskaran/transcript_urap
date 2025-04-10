import os
import base64
import csv
from PyPDF2 import PdfReader, PdfWriter
from dotenv import load_dotenv
from anthropic import Anthropic
import random
import time

load_dotenv()
# Claude client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))



def split_pdf(input_pdf_path, output_dir, pages_per_split=5):
    os.makedirs(output_dir, exist_ok=True)
    reader = PdfReader(input_pdf_path)
    total_pages = len(reader.pages)
    split_paths = []

    for start in range(0, total_pages, pages_per_split):
        writer = PdfWriter()
        for i in range(start, min(start + pages_per_split, total_pages)):
            writer.add_page(reader.pages[i])
        out_path = os.path.join(output_dir, f"split_{start // pages_per_split + 1}.pdf")
        with open(out_path, "wb") as f:
            writer.write(f)
        split_paths.append(out_path)

    return split_paths


def call_claude_with_pdf(pdf_path, prompt):
    with open(pdf_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": encoded,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )

    if message.content:
        return message.content[0].text
    else:
        print("❌ Claude API returned no content.")
        return ""


def extract_tables_from_text(text_response):
    tables = []
    current = []
    for line in text_response.strip().splitlines():
        if line.strip() == "":
            if current:
                tables.append(current)
                current = []
        else:
            current.append([cell.strip() for cell in line.split(",")])
    if current:
        tables.append(current)
    return tables


def save_table_to_csv(table, output_csv_path):
    with open(output_csv_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(table)


def method_claude_sdk_pipeline(pdf_path, output_folder, pages_per_split=5):
    os.makedirs(output_folder, exist_ok=True)
    split_dir = os.path.join(output_folder, "splits")
    split_files = split_pdf(pdf_path, split_dir, pages_per_split)

    csv_files = []
    table_index = 1
    for split_pd in split_files:
        print(f"Processing: {split_pd}")
        text = call_claude_with_pdf(
            split_pd, "Extract all tables as CSV. No explanation, just raw CSV."
        )
        tables = extract_tables_from_text(text)
        for table in tables:
            csv_path = os.path.join(output_folder, f"claude_table_{table_index}.csv")
            save_table_to_csv(table, csv_path)
            csv_files.append(csv_path)
            print(f"✔ Saved: {csv_path}")
            table_index += 1
        sleep_time = random.uniform(1.5, 3.5)
        print(f"⏳ Sleeping for {sleep_time:.2f} seconds before next request...")
        time.sleep(sleep_time)
