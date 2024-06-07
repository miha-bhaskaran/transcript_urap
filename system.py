from pdf_png_1 import pdfPngConverter
from vision_script_2 import vision
from csv_concat_3 import concatenate_csv_files
from preProcess_4 import find_matching_lines
from aws_script_2 import process_images_in_folder
from postProcessOpenAI_5 import extract_course_info_2
from postProcessRegex import regex_post_process
from postProcess_4o import post_process_4o
from gpt_4o_2 import vision_4


def visionNoZSL(transcript_name, output_folder, orig):
    output_folder = output_folder+"_no_zsl"
    # STEP 1: Convert PDF to Folder of PNGs
    pdfPngConverter(transcript_name, output_folder)
   

    #STEP 2: Run Vision or AWS on folder

    vision(output_folder)

    #STEP 3: Concatenate all PNGs
    concatenate_csv_files(output_folder)

    #STEP 4: Find match percentage of pre-preprocess
    print(output_folder, "PRE PROCESS MATCH:")
    find_matching_lines(output_folder + '/' + output_folder + '_combined.csv', 'validation/'+ orig + '.csv')

    #STEP 5: Find match percentage for post-processed numbers
    post(output_folder ,orig)

def awsBoto(transcript_name, output_folder, orig):
    output_folder = output_folder + "awsBoto"
    # STEP 1: Convert PDF to Folder of PNGs
    pdfPngConverter(transcript_name, output_folder)
    

    #STEP 2: Run Vision or AWS on folder
    process_images_in_folder(output_folder)
    

    #STEP 3: Concatenate all PNGs
    concatenate_csv_files(output_folder)

    #STEP 4: Find match percentage of pre-preprocess
    print(output_folder, "PRE PROCESS MATCH:")
    find_matching_lines(output_folder + '/' + output_folder + '_combined.csv', 'validation/'+ orig + '.csv')

    #STEP 5: Find match percentage for post-processed numbers
    post(output_folder ,orig)

def visionZSL(transcript_name, output_folder, orig):
    
    output_folder = output_folder + "ZSL"
    # STEP 1: Convert PDF to Folder of PNGs
    pdfPngConverter(transcript_name, output_folder)
   

    #STEP 2: Run Vision or AWS on folder

    vision_4(output_folder, 'output_png.csv', 'transcriptmiha')

    #STEP 3: Concatenate all PNGs
    concatenate_csv_files(output_folder)

    #STEP 4: Find match percentage of pre-preprocess
    print(output_folder, "PRE PROCESS MATCH:")
    find_matching_lines(output_folder + '/' + output_folder + '_combined.csv', 'validation/'+ orig + '.csv')

    #STEP 5: Find match percentage for post-processed numbers
    post(output_folder ,orig)


    
def post(output_folder, orig):

    print(output_folder, "open 4o ---------------------------------------------------------------------------")
    post_process_4o('input_example.csv', 'output_example.csv', output_folder)
    find_matching_lines(output_folder + '/' +'Final_post_processed_gpt4o.csv', 'validation/'+ orig + '.csv')
    print(output_folder, "---------------------------------------------------------------------------")
    #REGEX SYSTEM
    regex_post_process(output_folder)
    # post_process_2 - open ai + regex
    print(output_folder, "regex ---------------------------------------------------------------------------")
    find_matching_lines(output_folder + '/' +'FINAL_post_process_REGEX.csv', 'validation/'+ orig + '.csv')
    print("---------------------------------------------------------------------------------------------")
    extract_course_info_2(output_folder)
    # post_process_2 - open ai + open ai
    print(output_folder, "OPEN AI  ---------------------------------------------------------------------------")
    find_matching_lines(output_folder + '/' +'FINAL_post_process_OPEN_AI.csv', 'validation/'+ orig + '.csv')
    print("---------------------------------------------------------------------------------------------")
    # FINAL_post_process_3 - open ai + open ai + regex
    print(output_folder, "OPEN AI  + regex")
    find_matching_lines(output_folder + '/' +'FINAL_post_process_COMBO.csv', 'validation/'+ orig + '.csv')
    print("---------------------------------------------------------------------------------------------")


# output_folder = ['asu', 'dickonson_uni', 'edmonds', 'g_r', 'taylor','trans', 'uva', 'va', 'west_mich']
# transcript_name = ['transcripts/asu', 'transcripts/dickonson_uni', 'transcripts/edmonds', 'transcripts/g_r', 'transcripts/taylor','transcripts/trans', 'transcripts/uva', 'transcripts/va', 'transcripts/west_mich']

output_folder = ['asu', 'dickonson_uni', 'edmonds']
transcript_name = ['transcripts/asu', 'transcripts/dickonson_uni', 'transcripts/edmonds']


for i in range(len(output_folder)):
    visionNoZSL(transcript_name[i], output_folder[i], output_folder[i])
    #awsBoto(transcript_name[i], output_folder[i], output_folder[i])
    #visionZSL(transcript_name[i], output_folder[i], output_folder[i])

    #post(transcript_name[i], output_folder[i])
