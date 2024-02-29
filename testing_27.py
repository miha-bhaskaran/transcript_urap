import json
import boto3
import pandas as pd
import re

from parser_1 import (
    map_word_id,
    extract_table_info
)


def lambda_handler(bucketname, filename):
    textract = boto3.client("textract")
    print(f"Bucket: {bucketname} ::: Key: {filename}")

    response = textract.analyze_document(
        Document={
            "S3Object": {
                "Bucket": bucketname,
                "Name": filename,
            }
        },
        FeatureTypes=["FORMS", "TABLES"],
    )


    word_map = map_word_id(response)
    table = extract_table_info(response, word_map)

    return (table)



def table_to_csv(table_name, data):

    df = pd.DataFrame(data[1:], columns=data[0])
    csv_file_name = f"{table_name}.csv"

    print(f"Generated CSV: {csv_file_name}")
    return csv_file_name, df

def table_regex(name, df):
    # capture anything that starts with cou and gr case insensitive
    pattern = '(?i)(cou|gr|cla)\w*(\s+\w+)*|Gr(?:ade|d)?'
    #pattern = '(?i)\b(cou|gr|cla)\w*(\s+\w+)*|Gr(?:ade|d)?'

 
    filtered_df = df.filter(regex=pattern, axis=1)

    filtered_df.to_csv(name, index=False)
    return filtered_df

# Supports only PNG??
bucketname = "transcriptmiha"
#documentName = "sampleNotes.pdf"
filename = "trans.png"
#filename = "uva_transcript.pdf"
#filename = 'west_mich.png'
#filename = 'uva.png'
tables = lambda_handler(bucketname, filename)

for table_name, data in tables.items():
    #print(table_name)
    name, data_f = table_to_csv(table_name, data)
    print(table_regex(name, data_f))


