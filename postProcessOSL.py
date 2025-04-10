import openai
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)

openai.api_key = config["OPENAI_API_KEY"]


def remove_backtick_symbols(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    cleaned_content = content.replace("`", "")
    with open(file_path, "w") as file:
        file.write(cleaned_content)


def post_process_OSL(input_example_path, output_example_path, folder):
    input_example_path = "input_example.csv"
    output_example_path = "output_example.csv"
    input_csv_path = folder + "/" + folder + "_combined.csv"
    output_csv_path = folder + "/" + "Final_post_processed_gpt4o.csv"

    
    with open(input_example_path, "r") as file:
        input_example_content = file.read()
    with open(output_example_path, "r") as file:
        output_example_content = file.read()
    with open(input_csv_path, "r") as file:
        csv_data = file.read()
    prompt = f"""
Here is an example of the input data:
{input_example_content}

Here is an example of the desired output format:
{output_example_content}

The above are just examples to show formatting. The CSV data is as follows:
{csv_data}

Please extract only the course IDs and their corresponding grades from the data above, and output them in the same format as the example. Do not include any other text.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant extracting course IDs and grades into clean CSV format.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=2000,
        temperature=0.3,
    )

    processed_data = response.choices[0].message["content"].strip()

    with open(output_csv_path, "w") as file:
        file.write(processed_data)

    remove_backtick_symbols(output_csv_path)

    print(f"Extracted data saved to {output_csv_path}")
