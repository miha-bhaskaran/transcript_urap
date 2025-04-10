import os
from dotenv import load_dotenv
from csvConcatenation import concatenate_csv_files
from matchPercentage import match_percentage
from postProcessRegex import regex_post_process
from postProcessOSL import post_process_OSL
from methodClaude import method_claude_sdk_pipeline
from methodO1 import methodO1
from methodAWSpdf import process_pdfs_in_folder
from missingCourses import find_missing_courses

# Load .env file
load_dotenv()

def method_awsBoto(transcript_name, output_folder, orig):
    orig = output_folder
    output_folder = output_folder + "awsBoto"
    os.makedirs(output_folder, exist_ok=True)

    process_pdfs_in_folder(transcript_name, output_folder)
    concatenate_csv_files(output_folder)

    file_a = output_folder + "/" + output_folder + "_combined.csv"
    file_b = "validation/" + orig + ".csv"
    output = output_folder + "/MISSING_courses.csv"
    output2 = output_folder + "/MATCHED_courses.csv"

    find_missing_courses(
        file_a, file_b, output, output2, course_threshold=80, grade_threshold=70
    )
    post_process_method(output_folder, orig)


def method_claude(transcript_name, output_folder, orig):
    output_folder = output_folder + "claude"
    os.makedirs(output_folder, exist_ok=True)

    pdf_path = transcript_name + ".pdf"
    method_claude_sdk_pipeline(pdf_path=pdf_path, output_folder=output_folder)

    concatenate_csv_files(output_folder)

    file_a = output_folder + "/" + output_folder + "_combined.csv"
    file_b = "validation/" + orig + ".csv"
    output = output_folder + "/MISSING_courses.csv"
    output2 = output_folder + "/MATCHED_courses.csv"

    find_missing_courses(
        file_a, file_b, output, output2, course_threshold=80, grade_threshold=70
    )
    post_process_method(output_folder, orig)


def method_o1(transcript_name, output_folder, orig):
    output_folder = output_folder + "o1"
    os.makedirs(output_folder, exist_ok=True)

    # Safely retrieve API key from environment
    api_key = os.getenv("GPT4O_API_KEY")
    if not api_key:
        raise ValueError("Missing GPT4O_API_KEY in environment.")

    pdf_path = transcript_name + ".pdf"
    methodO1(pdf_path, api_key, output_folder)

    concatenate_csv_files(output_folder)

    file_a = output_folder + "/" + output_folder + "_combined.csv"
    file_b = "validation/" + orig + ".csv"
    output = output_folder + "/MISSING_courses.csv"
    output2 = output_folder + "/MATCHED_courses.csv"

    find_missing_courses(
        file_a, file_b, output, output2, course_threshold=60, grade_threshold=50
    )
    post_process_method(output_folder, orig)



def post_process_method(output_folder, orig):

    # REGEX
    regex_post_process(output_folder)
    print(
        output_folder,
        "regex ---------------------------------------------------------------------------",
    )
    # match_percentage(output_folder + '/' +'FINAL_post_process_REGEX.csv', 'testing_validation/'+ orig + '.csv')
    match_percentage(
        output_folder + "/" + "FINAL_post_process_REGEX.csv",
        "validation/" + orig + ".csv",
    )
    print(
        "---------------------------------------------------------------------------------------------"
    )

    # OSL
    print(
        output_folder,
        "open 4o OSL ---------------------------------------------------------------------------",
    )
    post_process_OSL("input_example.csv", "output_example.csv", output_folder)
    # match_percentage(output_folder + '/' +'Final_post_processed_gpt4o.csv', 'testing_validation/'+ orig + '.csv')
    match_percentage(
        output_folder + "/" + "Final_post_processed_gpt4o.csv",
        "validation/" + orig + ".csv",
    )
    print(
        output_folder,
        "---------------------------------------------------------------------------",
    )


output_folder = [
    "asu",
    "dickonson_uni",
    "edmonds",
    "g_r",
    "taylor",
    "trans",
    "uva",
    "va",
    "west_mich",
]
transcript_name = [
    "transcripts/asu",
    "transcripts/dickonson_uni",
    "transcripts/edmonds",
    "transcripts/g_r",
    "transcripts/taylor",
    "transcripts/trans",
    "transcripts/uva",
    "transcripts/va",
    "transcripts/west_mich",
]


# output_folder = ['depaul', 'mich_state_uni', 'suny', 'kutztown_upenn', 'wayne','western_mich_uni']
# transcript_name = ['testing_transcripts/depaul', 'testing_transcripts/mich_state_uni', 'testing_transcripts/suny', 'testing_transcripts/kutztown_upenn', 'testing_transcripts/wayne','testing_transcripts/western_mich_uni']

# output_folder = ['wayne']
# transcript_name = ['testing_transcripts/wayne']

# output_folder = ['herkimer_SUNY']
# transcript_name = ['testing_transcripts/herkimer_SUNY']


# testing


for i in range(len(output_folder)):

    method_awsBoto(transcript_name[i], output_folder[i], output_folder[i])
    method_o1(transcript_name[i], output_folder[i], output_folder[i])
    method_claude(transcript_name[i], output_folder[i], output_folder[i])
