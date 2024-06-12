import boto3
import csv
import os

def extract_text_from_image(image_path):
    # Initialize the Textract client
    textract = boto3.client('textract')

    # Load the image
    with open(image_path, 'rb') as document:
        image_bytes = document.read()

    # Call Textract to analyze the document
    response = textract.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['TABLES', 'FORMS']
    )

    return response

def extract_tables_from_response(response):
    blocks = response['Blocks']
    tables = [block for block in blocks if block['BlockType'] == 'TABLE']

  

    extracted_tables = []

    for table in tables:
        rows = {}
        for relationship in table['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    cell = next(block for block in blocks if block['Id'] == child_id)
                    if cell['BlockType'] == 'CELL':
                        row_index = cell['RowIndex']
                        col_index = cell['ColumnIndex']
                        if row_index not in rows:
                            rows[row_index] = {}
                        rows[row_index][col_index] = cell

        table_data = []
        max_col_index = max(max(row.keys()) for row in rows.values())
        for row_index in sorted(rows.keys()):
            row_data = []
            for col_index in range(1, max_col_index + 1):
                if col_index in rows[row_index]:
                    text = ''
                    for relationship in rows[row_index][col_index].get('Relationships', []):
                        if relationship['Type'] == 'CHILD':
                            for child_id in relationship['Ids']:
                                word = next(block for block in blocks if block['Id'] == child_id)
                                if word['BlockType'] == 'WORD':
                                    text += word['Text'] + ' '
                    text = text.strip()
                
                else:
                    text = ''
                row_data.append(text)
            table_data.append(row_data)

        extracted_tables.append(table_data)

    return extracted_tables

def save_tables_to_csv(tables, csv_filename):
    with open(csv_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for table in tables:
            for row in table:
                csvwriter.writerow(row)
            csvwriter.writerow([])  # Add an empty row between tables

def process_images_in_folder(folder_path):
    # List all files in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.png'):
            image_path = os.path.join(folder_path, filename)
            csv_filename = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.csv")

            # Extract text from image
            response = extract_text_from_image(image_path)

            # Extract tables
            tables = extract_tables_from_response(response)

    

            # Save the tables to a CSV file
            save_tables_to_csv(tables, csv_filename)
            print(f"Extracted tables from {filename} have been saved to {csv_filename}")

