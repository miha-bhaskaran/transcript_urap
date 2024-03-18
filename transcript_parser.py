import json
import boto3
import pandas as pd
import re
import os
import time
from datetime import datetime


from parser_1 import (
    map_word_id,
    extract_table_info
)

def wait_for_textract_job_completion(textract_client, job_id):
    all_pages_blocks = []
    next_token = None
    while True:
        if next_token:
            response = textract_client.get_document_analysis(JobId=job_id, NextToken=next_token)
        else:
            response = textract_client.get_document_analysis(JobId=job_id)

        status = response.get('JobStatus')
        if status in ['SUCCEEDED', 'PARTIAL_SUCCESS']:
            all_pages_blocks.extend(response.get('Blocks', []))
            next_token = response.get('NextToken')
            if not next_token:
                break  # Exit loop if there's no NextToken
        elif status == 'FAILED':
            raise Exception(f"Textract job {job_id} failed.")
        else:
            time.sleep(5)  # Sleep to avoid hitting rate limits

    return {'Blocks': all_pages_blocks}

def lambda_handler(bucketname, filename):
    textract = boto3.client('textract')
    
    if filename.lower().endswith('.pdf'):
        response = textract.start_document_analysis(
            DocumentLocation={"S3Object": {"Bucket": bucketname, "Name": filename}},
            FeatureTypes=["FORMS", "TABLES"],
        )
        job_id = response['JobId']
        print(f"Started job with id: {job_id}")
        response = wait_for_textract_job_completion(textract, job_id)
    else:  # For non-PDF files, this path will not properly handle multi-page documents.
        response = textract.analyze_document(
            Document={"S3Object": {"Bucket": bucketname, "Name": filename}},
            FeatureTypes=["FORMS", "TABLES"],
        )
        response = {'Blocks': response.get('Blocks', [])}  # Ensure consistent format

    word_map = map_word_id(response)
    table = extract_table_info(response, word_map)
    return table

def table_to_csv(table_name, data, pattern='(?i)(sub|cou|gr|cla)[\w.]*((\s+[\w.]+)*)|Gr(?:ade|d)?'):
    # fix the regex it matches part of undergraduate stuff
    df = pd.DataFrame(data[1:], columns=data[0])
    # Filter columns by regex
    filtered_df = df.filter(regex=pattern)
    if filtered_df.empty:
        print(f"Skipping empty table: {table_name}")
        return None
    csv_file_name = f"{table_name}.csv"
    filtered_df.to_csv(csv_file_name, index=False)
    print(f"Generated CSV: {csv_file_name}")
    return csv_file_name


def concat(table_names, output_filename):
    dfs = []
    for file in table_names:
        try:
            df = pd.read_csv(file)
            dfs.append(df)
        except pd.errors.EmptyDataError:
            print(f"File {file} is empty or invalid, skipping.")
    if dfs:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS
        output_filename = f"{filename}_{timestamp}.csv"
        concatenated_df = pd.concat(dfs, ignore_index=True)
        concatenated_df.to_csv(output_filename, index=False)
        print(f"Concatenated CSV: {output_filename}")

# Change this variable name outside of the functions to avoid scope issues
output_filename = "combined_transcript_data"

bucketname = "transcriptmiha"
#filename = "uva_transcript.pdf"
#filename = 'west_mich.png'
# filename = "asu.pdf"
#filename = "dickonson_uni.pdf"
# filename = "edmonds_community_college.pdf"
# filename = "grand_rapids_community_college.png"
#filename = "taylor_unv.pdf"
#filename = "transcript.pdf"
# filename = "va_com_college.pdf"
filename = "western_mihc_transcript.pdf"
tables = lambda_handler(bucketname, filename)
table_names = []

for table_name, data in tables.items():
    csv_file_name = table_to_csv(table_name, data)
    if csv_file_name:
        table_names.append(csv_file_name)

concat(table_names, output_filename)
