# prompts.py

# Define the prompts
OPENAI_API_KEY = "sk-proj-D8cDwYGshUI9e4Qp7f4sT3BlbkFJIA67ZqaOxnvQ0Pc8hZT8"

SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are a helpful assistant that extracts course ID and grades from the given input and outputs it in a CSV format.",
}

USER_PROMPT_EXAMPLE = "Here is an example of the formatting of a desired output:\n\nExample OUTPUT:\n{example_csv_text}\n\nUsing this example, extract course ids and grades earned from the following image and output them in CSV format without any additional explanations or text. Capture the course name exactly. Grades are typically A,B,C,D,F, P, NP with +/-. Include special characters. Do not add any extra characters."

USER_PROMPT_EXAMPLE_IMAGE = {
    "role": "user",
    "content": "Below is the example image:",
    "name": "example_image",
    "type": "image",
    "image_url": None,  
}

USER_PROMPT_PROCESS_IMAGE = {
    "role": "user",
    "content": "Below is the image to process:",
    "name": "process_image",
    "type": "image",
    "image_url": None, 
}

SYSTEM_PROMPT_ZSL = "Extract only course ids and grades earned from the image and output them in CSV format without any additional explanations or text. Capture the course name exactly. Grades are typically A,B,C,D,F, P, NP with +/-.  Include special characters. Do not add any extra characters."


def get_user_prompt(chunk):
    return f"""
    Given the following cleaned CSV data, extract and list all course IDs and the corresponding grades. nUsing this example, extract course ids and grades earned from the following image and output them in CSV format without any additional explanations or text. Capture the course name exactly. Grades are typically A,B,C,D,F, P, NP with +/-. Include special characters. Do not add any extra characters.
    The CSV data is as follows:

    {chunk}

    Please output the data in a clean format with two columns: 'COURSE' and 'GRADE'.
    """
