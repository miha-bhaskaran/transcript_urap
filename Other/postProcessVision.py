import openai
import re
import json
from prompts import SYSTEM_PROMPT, get_user_prompt


with open("config.json", "r") as config_file:
    config = json.load(config_file)

openai.api_key = config["OPENAI_API_KEY_1"]


def clean_csv_data(csv_data):
    cleaned_data = re.sub(r"[^\w\s,]", "", csv_data)
    return cleaned_data


def process_chunk(chunk):
    prompt = get_user_prompt(chunk)
    response = openai.ChatCompletion.create(
        model="gpt-4o-2024-05-13",
        messages=[SYSTEM_PROMPT, {"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.3,
    )

    output = response.choices[0].message["content"].strip()
    return output


def extract_course_info(folder_name):
    path_to_open = folder_name + "/" + folder_name + "_combined.csv"
    output_path1 = folder_name + "/" + "FINAL_post_process_OPEN_AI.csv"
    with open(path_to_open, "r") as file:
        csv_data = file.read()
    cleaned_csv_data = clean_csv_data(csv_data)
    lines = cleaned_csv_data.split("\n")
    chunk_size = 100  # Adjust the chunk size as needed
    chunks = [lines[i : i + chunk_size] for i in range(0, len(lines), chunk_size)]
    results = []
    for chunk in chunks:
        chunk_text = "\n".join(chunk)
        result = process_chunk(chunk_text)
        results.append(result)
    final_output = "\n".join(results)
    with open(output_path1, "w") as file:
        file.write(final_output)

    print(f"Extracted data saved to {output_path1}")
    extract_course_info_2(folder_name, output_path1)


def extract_course_info_2(folder_name, output_path1):

    output_path2 = folder_name + "/" + "FINAL_post_process_COMBO.csv"

    with open(output_path1, "r") as file:
        csv_data = file.read()
    csv_data = re.sub(r"\|", "", csv_data)
    lines = csv_data.split("\n")
    cleaned_data = []
    for line in lines:
        matches = re.findall(r"\b[a-zA-Z0-9.&+-]+\b", line)
        if len(matches) >= 2:
            course = " ".join(matches[:-1])
            grade = matches[-1]
            cleaned_data.append(f"{course},{grade}")

    with open(output_path2, "w") as file:
        file.write("\n".join(cleaned_data))

    print(f"Final cleaned data saved to {output_path2}")
