import os
import csv
import openai
from PyPDF2 import PdfReader


def extract_text_with_pypdf2(pdf_path):
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"
    return full_text.strip()


def extract_tables_with_gpt4o_text(api_key, pdf_text):
    openai.api_key = api_key

    prompt = f"""
Extract all tables from the following transcript and return each table as plain CSV-formatted rows.
Separate tables with empty lines. No explanations or extra commentary.

Transcript:
{pdf_text}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
        temperature=0.3,
    )

    tables = []
    current_table = []

    try:
        text_response = response.choices[0].message["content"]
        for line in text_response.strip().splitlines():
            if not line.strip():
                if current_table:
                    tables.append(current_table)
                    current_table = []
            else:
                row = [cell.strip() for cell in line.split(",")]
                current_table.append(row)
        if current_table:
            tables.append(current_table)

        return tables
    except Exception as e:
        print("❌ Error parsing GPT-4o response:", e)
        return []


def save_table_to_csv(table, csv_path):
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(table)


def methodO1(pdf_path, api_key, output_path):
    print(f"📄 Extracting text from: {pdf_path}")
    text_data = extract_text_with_pypdf2(pdf_path)

    print(f"⚙️ Sending extracted text to GPT-4o for table parsing...")
    tables = extract_tables_with_gpt4o_text(api_key, text_data)

    os.makedirs(output_path, exist_ok=True)
    for i, table in enumerate(tables):
        csv_name = (
            f"{os.path.splitext(os.path.basename(pdf_path))[0]}_gpto1_table_{i + 1}.csv"
        )
        csv_path = os.path.join(output_path, csv_name)
        save_table_to_csv(table, csv_path)
        print(f"✔ Saved table {i + 1} to {csv_path}")
