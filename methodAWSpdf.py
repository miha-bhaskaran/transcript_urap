import boto3
import os
import time
import csv
from csvConcatenation import concatenate_csv_files


textract = boto3.client("textract")
s3 = boto3.client("s3")


S3_BUCKET = "transcriptmiha"


def upload_pdf_to_s3(file_path, bucket, object_name):
    with open(file_path, "rb") as file_data:
        s3.upload_fileobj(file_data, bucket, object_name)
    return object_name


def start_textract_job(bucket, document_name):
    response = textract.start_document_analysis(
        DocumentLocation={"S3Object": {"Bucket": bucket, "Name": document_name}},
        FeatureTypes=["TABLES"],
    )
    return response["JobId"]


def wait_for_job(job_id):
    while True:
        response = textract.get_document_analysis(JobId=job_id)
        status = response["JobStatus"]
        if status == "SUCCEEDED":
            return
        elif status == "FAILED":
            raise Exception("Textract job failed.")
        time.sleep(5)


def get_full_textract_result(job_id):
    pages = []
    next_token = None
    while True:
        if next_token:
            response = textract.get_document_analysis(
                JobId=job_id, NextToken=next_token
            )
        else:
            response = textract.get_document_analysis(JobId=job_id)
        pages.append(response)
        next_token = response.get("NextToken")
        if not next_token:
            break
    return pages


def extract_tables_from_response(response):
    blocks = response["Blocks"]
    tables = [block for block in blocks if block["BlockType"] == "TABLE"]
    extracted_tables = []

    for table in tables:
        rows = {}
        for relationship in table.get("Relationships", []):
            if relationship["Type"] == "CHILD":
                for child_id in relationship["Ids"]:
                    cell = next(
                        (block for block in blocks if block["Id"] == child_id), None
                    )
                    if cell and cell["BlockType"] == "CELL":
                        row_idx = cell["RowIndex"]
                        col_idx = cell["ColumnIndex"]
                        if row_idx not in rows:
                            rows[row_idx] = {}
                        rows[row_idx][col_idx] = cell

        table_data = []
        max_col_index = max((max(row.keys()) for row in rows.values()), default=0)
        for row_idx in sorted(rows.keys()):
            row_data = []
            for col_idx in range(1, max_col_index + 1):
                text = ""
                cell = rows[row_idx].get(col_idx)
                if cell:
                    for rel in cell.get("Relationships", []):
                        if rel["Type"] == "CHILD":
                            for child_id in rel["Ids"]:
                                word = next(
                                    (
                                        b
                                        for b in blocks
                                        if b["Id"] == child_id
                                        and b["BlockType"] == "WORD"
                                    ),
                                    None,
                                )
                                if word:
                                    text += word["Text"] + " "
                row_data.append(text.strip())
            table_data.append(row_data)

        extracted_tables.append(table_data)
    return extracted_tables


def save_table_to_csv(table, csv_filename):
    with open(csv_filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for row in table:
            writer.writerow(row)


def process_pdfs_in_folder(pdf_path, output_folder, delete_after=True):
    filename = os.path.basename(pdf_path)
    name_no_ext = os.path.splitext(filename)[0]


    os.makedirs(output_folder, exist_ok=True)

    object_name = f"textract_uploads/{filename}"


    upload_pdf_to_s3(pdf_path + ".pdf", S3_BUCKET, object_name)
    print(f"Uploaded {filename} to S3. Starting Textract analysis...")


    job_id = start_textract_job(S3_BUCKET, object_name)
    wait_for_job(job_id)
    responses = get_full_textract_result(job_id)


    table_count = 1
    for response in responses:
        tables = extract_tables_from_response(response)
        for table in tables:
            csv_filename = os.path.join(
                output_folder, f"{name_no_ext}_table_{table_count}.csv"
            )
            save_table_to_csv(table, csv_filename)
            print(f"Saved table {table_count} to {csv_filename}")
            table_count += 1

    # detele from aws

    if delete_after:
        print(f"Deleting {object_name} from S3...")
        s3.delete_object(Bucket=S3_BUCKET, Key=object_name)
        print("Deleted.")
