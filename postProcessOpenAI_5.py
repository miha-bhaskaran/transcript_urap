import openai
import re

# Initialize the OpenAI API
openai.api_key = 'sk-proj-D8cDwYGshUI9e4Qp7f4sT3BlbkFJIA67ZqaOxnvQ0Pc8hZT8'

def clean_csv_data(csv_data):
    # Remove any weird dashes or extra characters
    cleaned_data = re.sub(r'[^\w\s,]', '', csv_data)
    return cleaned_data

def process_chunk(chunk):
    # Define the prompt for the model
    prompt = f"""
    Given the following cleaned CSV data, extract and list all course IDs and the corresponding grades. Grades will either be letters or numbers.
    The CSV data is as follows:

    {chunk}

    Please output the data in a clean format with two columns: 'COURSE' and 'GRADE'.
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
    output = response.choices[0].message['content'].strip()
    return output

def extract_course_info_2(folder_name):
    path_to_open = folder_name + '/' + folder_name + '_combined.csv'
    output_path1 = folder_name + "/" + "FINAL_post_process_OPEN_AI.csv"

    # Read the CSV file as raw text
    with open(path_to_open, 'r') as file:
        csv_data = file.read()

    # Clean the CSV data
    cleaned_csv_data = clean_csv_data(csv_data)

    # Split the cleaned data into chunks
    lines = cleaned_csv_data.split('\n')
    chunk_size = 100  # Adjust the chunk size as needed
    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

    # Process each chunk and collect results
    results = []
    for chunk in chunks:
        chunk_text = '\n'.join(chunk)
        result = process_chunk(chunk_text)
        results.append(result)

    # Combine results and write to the output file
    final_output = '\n'.join(results)
    with open(output_path1, 'w') as file:
        file.write(final_output)

    print(f"Extracted data saved to {output_path1}")
    extract_course_info3(folder_name, output_path1)

def extract_course_info3(folder_name, output_path1):

    output_path2 = folder_name + "/" + "FINAL_post_process_COMBO.csv"

    with open(output_path1, 'r') as file:
        csv_data = file.read()

    # Remove unwanted characters
    csv_data = re.sub(r'\|', '', csv_data)
    lines = csv_data.split('\n')
    cleaned_data = []
    for line in lines:
        matches = re.findall(r'\b[a-zA-Z0-9.&+-]+\b', line)
        if len(matches) >= 2:
            course = ' '.join(matches[:-1])
            grade = matches[-1]
            cleaned_data.append(f"{course},{grade}")

    # Write the cleaned data to a new CSV file
    with open(output_path2, 'w') as file:
        file.write('\n'.join(cleaned_data))

    print(f"Final cleaned data saved to {output_path2}")


