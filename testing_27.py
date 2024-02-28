import json
import boto3
import pandas as pd
from pprint import pprint
from parser_1 import (
    extract_text,
    map_word_id,
    extract_table_info,
    get_key_map,
    get_value_map,
    get_kv_map,
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

    #print(json.dumps(response))

    #raw_text = extract_text(response, extract_by="LINE")
    word_map = map_word_id(response)
    table = extract_table_info(response, word_map)
    #key_map = get_key_map(response, word_map)
    #value_map = get_value_map(response, word_map)
    #final_map = get_kv_map(key_map, value_map)

    #print(json.dumps(table))
    #print(json.dumps(final_map))
    #print(raw_text)
    print(table)
    return (table)

    #return {"statusCode": 200, "body": json.dumps("Thanks from Srce Cde!")}

def table_to_csv(table_name, data):
    # Convert the list of lists to a DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])
    
    # Generate a CSV file name based on the table name
    csv_file_name = f"{table_name}.csv"
    
    # Export the DataFrame to CSV
    df.to_csv(csv_file_name, index=False)
    print(f"Generated CSV: {csv_file_name}")


# Only png??
bucketname = "transcriptmiha"
#documentName = "sampleNotes.pdf"
#filename = "trans.png"
#filename = "uva_transcript.pdf"
filename = "uva.png"
tables = lambda_handler(bucketname, filename)

for table_name, data in tables.items():
    table_to_csv(table_name, data)


