import os
import openai
import re

# OpenAI API Key
api_key = "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"  # Replace with your actual API key
openai.api_key = api_key


def remove_backtick_symbols(file_path):
    # Read the file content
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Remove backtick symbols
    cleaned_content = content.replace('`', '')

    # Write the cleaned content back to the file
    with open(file_path, 'w') as file:
        file.write(cleaned_content)


def post_process_4o(input_example_path, output_example_path, folder):
    input_example_path = 'input_example.csv'
    output_example_path = 'output_example.csv'
    input_csv_path =  folder+ "/" + folder + "_combined.csv"
    output_csv_path = folder+ "/"+ 'Final_post_processed_gpt4o.csv'

    # Read the input and output example files
    with open(input_example_path, "r") as file:
        input_example_content = file.read()

    with open(output_example_path, "r") as file:
        output_example_content = file.read()

    # Read the CSV file as raw text
    with open(input_csv_path, 'r') as file:
        csv_data = file.read()
    
    # Define the prompt for the model
    prompt = f"""
    Here is an example of the input data:
    {input_example_content}

    Here is an example of the desired output format:
    {output_example_content}

    The above are just examples to show formatting. The CSV data is as follows:
    {csv_data}

    Extract the course IDs and the grades and format it like the output example. Do not include any other information.
    """

    # Call the OpenAI API to process the data
    response = openai.ChatCompletion.create(
        model="gpt-4o-2024-05-13",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who is tasked with extracting only the course id and corresponding grade of any given file."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.3
    )

    # Extract the response text
    processed_data = response.choices[0].message['content'].strip()

    # Write the processed data to the output file
    with open(output_csv_path, 'w') as file:
        file.write(processed_data)

    remove_backtick_symbols(output_csv_path)

    print(f"Extracted data saved to {output_csv_path}")




