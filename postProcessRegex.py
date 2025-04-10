import openai
import json
import re

with open("config.json", "r") as config_file:
    config = json.load(config_file)

openai.api_key = config["OPENAI_API_KEY_1"]


def regex_post_process(folder_name):
    path_to_open = folder_name + "/" + folder_name + "_combined.csv"

    output_path2 = folder_name + "/" + "FINAL_post_process_REGEX.csv"

    with open(path_to_open, "r") as file:
        csv_data = file.read()
    lines = csv_data.split("\n")
    # print(lines)
    cleaned_data = []
    for line in lines:
        matches = re.findall(r"\b[a-zA-Z0-9.&+-]+\b", line)
        # print(matches)
        if len(matches) >= 2:
            course = " ".join(matches[:-1])
            grade = matches[-1]
            cleaned_data.append(f"{course},{grade}")

    with open(output_path2, "w") as file:
        file.write("\n".join(cleaned_data))


