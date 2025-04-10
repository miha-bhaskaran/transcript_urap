from Other.pdfToPng import pdf_png_conversion
from Other.methodVisionZSL import vision_ZSL
from csvConcatenation import concatenate_csv_files
from matchPercentage import match_percentage
from Other.methodAWS import process_images_in_folder
from Other.postProcessVision import extract_course_info
from postProcessRegex import regex_post_process
from postProcessOSL import post_process_OSL
from methodVisionOSL import method_vision_osl
from Other.huggingFaceMethod import hugging_method
from Other.methodExtractTable import extractTable
from methodClaude import method_claude_sdk_pipeline
from methodO1 import methodO1
from methodAWSpdf import process_pdfs_in_folder
import os
from missingCourses import find_missing_courses


def method_vision_ZSL(transcript_name, output_folder, orig):
    output_folder = output_folder + "ZSL"

    
    pdf_png_conversion(transcript_name, output_folder)

   
    vision_ZSL(output_folder)

    
    concatenate_csv_files(output_folder)

    
    print(output_folder, "PRE PROCESS MATCH:")
    
    post_process_method(output_folder, orig)


def method_awsBoto(transcript_name, output_folder, orig):
    
    orig = output_folder

    output_folder = output_folder + "awsBoto"
    os.makedirs(output_folder, exist_ok=True)
  
    process_pdfs_in_folder(transcript_name, output_folder)

   
    concatenate_csv_files(output_folder)

    file_a = output_folder + "/" + output_folder + "_combined.csv"
    # file_b = "testing_validation/" + orig + ".csv"
    file_b = "validation/" + orig + ".csv"
    output = output_folder + "/MISSING_courses.csv"
    output2 = output_folder + "/MATCHED_courses.csv"

    find_missing_courses(
        file_a, file_b, output, output2, course_threshold=80, grade_threshold=70
    )

    # STEP 5: Find match percentage for post-processed numbers
    post_process_method(output_folder, orig)


def method_visioOSL(transcript_name, output_folder, orig):

    output_folder = output_folder + "OSL"
    
    pdf_png_conversion(transcript_name, output_folder)

    method_vision_osl(output_folder, "input_ex.png", "output_ex.csv", orig)

   
    concatenate_csv_files(output_folder)

    
    print(output_folder, "PRE PROCESS MATCH:")
    match_percentage(
        output_folder + "/" + output_folder + "_combined.csv",
        "testing_validation/" + orig + ".csv",
    )

   
    post_process_method(output_folder, orig)


def method_hugging(transcript_name, output_folder, orig):

    output_folder = output_folder
    
    pdf_png_conversion(transcript_name, output_folder)

    

    hugging_method(output_folder)

    
    concatenate_csv_files(output_folder)

    
    print(output_folder, "PRE PROCESS MATCH:")
    match_percentage(
        output_folder + "/" + output_folder + "_combined.csv",
        "testing_validation/" + orig + ".csv",
    )

   
    post_process_method(output_folder, orig)


def method_extractTable(transcript_name, output_folder, orig):

    output_folder = output_folder + "extractTable"
    # STEP 1: Convert PDF to Folder of PNGs

    pdf_png_conversion(transcript_name, output_folder)
    api_key = "86L2cv3UrotyBzUdpGFXHUC0ql12cqq4qiJG1awX"

    # STEP 2: Run Vision or AWS on folder
    extractTable(output_folder, api_key, output_folder)

    # STEP 3: Concatenate all PNGs
    concatenate_csv_files(output_folder)

    # STEP 4: Find match percentage of pre-preprocess
    print(output_folder, "PRE PROCESS MATCH:")
    match_percentage(
        output_folder + "/" + output_folder + "_combined.csv",
        "testing_validation/" + orig + ".csv",
    )

    # STEP 5: Find match percentage for post-processed numbers
    post_process_method(output_folder, orig)


# HERE


def method_claude(transcript_name, output_folder, orig):

    output_folder = output_folder + "claude"
    os.makedirs(output_folder, exist_ok=True)
    # # STEP 1: Convert PDF to Folder of PNGs

    # pdf_png_conversion(transcript_name, output_folder)
    api_key = "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"
    pdf_path = transcript_name + ".pdf"
    # STEP 2: Run claude
    method_claude_sdk_pipeline(pdf_path=pdf_path, output_folder=output_folder)

    # #STEP 3: Concatenate all PNGs
    concatenate_csv_files(output_folder)

    file_a = output_folder + "/" + output_folder + "_combined.csv"
    # file_b = "testing_validation/" + orig + ".csv"
    file_b = "validation/" + orig + ".csv"
    output = output_folder + "/MISSING_courses.csv"
    output2 = output_folder + "/MATCHED_courses.csv"

    is100 = find_missing_courses(
        file_a, file_b, output, output2, course_threshold=80, grade_threshold=70
    )
    if not (is100):
        post_process_method(output_folder, orig)



def method_o1(transcript_name, output_folder, orig):

    output_folder = output_folder + "o1"
    # STEP 1: Convert PDF to Folder of PNGs
    os.makedirs(output_folder, exist_ok=True)

    # pdf_png_conversion(transcript_name, output_folder)
    api_key = "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"

    # STEP 2:
    pdf_path = transcript_name + ".pdf"  # Full path to the PDF

    methodO1(pdf_path, api_key, output_folder)
    # methodO1(output_folder, api_key, output_folder)

    # STEP 3: Concatenate all PNGs
    concatenate_csv_files(output_folder)

    # STEP 4: Find match percentage of pre-preprocess
    file_a = output_folder + "/" + output_folder + "_combined.csv"
    # file_b = "testing_validation/" + orig + ".csv"
    file_b = "validation/" + orig + ".csv"
    output = output_folder + "/MISSING_courses.csv"
    output2 = output_folder + "/MATCHED_courses.csv"

    find_missing_courses(
        file_a, file_b, output, output2, course_threshold=60, grade_threshold=50
    )

    # print(output_folder, "PRE PROCESS MATCH:")
    # match_percentage(output_folder + '/' + output_folder + '_combined.csv', 'testing_validation/'+ orig + '.csv')

    # STEP 5: Find match percentage for post-processed numbers
    post_process_method(output_folder, orig)


def post_process_method(output_folder, orig):

    # REGEX SYSTEM
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

    # ZSL
    # extract_course_info(output_folder)
    # # post_process_2 - open ai + open ai
    # print(output_folder, "OPEN AI  ---------------------------------------------------------------------------")
    # match_percentage(output_folder + '/' +'FINAL_post_process_OPEN_AI.csv', 'testing_validation/'+ orig + '.csv')
    # print("---------------------------------------------------------------------------------------------")
    # # FINAL_post_process_3 - open ai + open ai + regex

    # COMBO
    # print(output_folder, "OPEN AI  + regex")
    # match_percentage(output_folder + '/' +'FINAL_post_process_COMBO.csv', 'testing_validation/'+ orig + '.csv')
    # print("---------------------------------------------------------------------------------------------")

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
    # method_hugging(transcript_name[i], output_folder[i], output_folder[i])
    # method_visioOSL(transcript_name[i], output_folder[i], output_folder[i])

    # method_extractTable(transcript_name[i], output_folder[i], output_folder[i])
    # method_claude(transcript_name[i], output_folder[i], output_folder[i])

    # post(transcript_name[i], output_folder[i])
