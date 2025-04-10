import json
import boto3
import pandas as pd
import re
import os
import time

from Other.parser_1 import map_word_id, extract_table_info


def wait_for_textract_job_completion(textract_client, job_id):
    while True:
        response = textract_client.get_document_analysis(JobId=job_id)
        status = response.get("JobStatus")
        if status == "SUCCEEDED":
            return response
        elif status in ["FAILED", "PARTIAL_SUCCESS"]:
            raise Exception(f"Textract job {job_id} failed with status {status}")
        time.sleep(5)  # Sleep to avoid hitting rate limits


def lambda_handler(bucketname, filename):
    textract = boto3.client("textract")

    if filename.lower().endswith(".pdf"):
        response = textract.start_document_analysis(
            DocumentLocation={"S3Object": {"Bucket": bucketname, "Name": filename}},
            FeatureTypes=["FORMS", "TABLES"],
        )
        job_id = response["JobId"]
        print(f"Started job with id: {job_id}")
        response = wait_for_textract_job_completion(textract, job_id)
    else:
        response = textract.analyze_document(
            Document={"S3Object": {"Bucket": bucketname, "Name": filename}},
            FeatureTypes=["FORMS", "TABLES"],
        )

    word_map = map_word_id(response)
    table = extract_table_info(response, word_map)
    return table


def table_to_csv(table_name, data):
    df = pd.DataFrame(data[1:], columns=data[0])
    if df.empty:
        print(f"Skipping empty table: {table_name}")
        return None
    csv_file_name = f"{table_name}.csv"
    df.to_csv(csv_file_name, index=False)
    print(f"Generated CSV: {csv_file_name}")
    return csv_file_name, df


def table_regex(name, df):
    # capture anything that starts with cou and gr case insensitive
    pattern = "(?i)(sub|cou|gr|cla)[\w.]*((\s+[\w.]+)*)|Gr(?:ade|d)?"
    # pattern = '(?i)\b(cou|gr|cla)\w*(\s+\w+)*|Gr(?:ade|d)?'

    filtered_df = df.filter(regex=pattern, axis=1)

    filtered_df.to_csv(name, index=False)
    return filtered_df


def concat(table_names):
    dfs = []
    for file in table_names:
        if not file:
            continue
        try:
            df = pd.read_csv(file)
            if not df.empty:
                dfs.append(df)
        except pd.errors.EmptyDataError:
            print(f"File {file} is empty or invalid, skipping.")
    if dfs:
        concatenated_df = pd.concat(dfs, ignore_index=True)
        concatenated_df.to_csv(filename + ".csv", index=False)
        print(f"Concatenated CSV: {filename}.csv")
    else:
        print("No data to concatenate.")


# Supports only PNG??
bucketname = "transcriptmiha"
# documentName = "sampleNotes.pdf"
# filename = "trans.png"
filename = "uva_transcript.pdf"
# filename = 'west_mich.png'
# filename = 'uva.png'
tables = lambda_handler(bucketname, filename)
table_names = []

for table_name, data in tables.items():
    x = table_name + ".csv"
    table_names.append(x)
    name, data_f = table_to_csv(table_name, data)
    print(table_regex(name, data_f))
    concat(table_names)
