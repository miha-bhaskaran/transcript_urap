from pdfToPng import pdf_png_conversion
from methodVisionZSL import vision_ZSL
from csvConcatenation import concatenate_csv_files
from matchPercentage import match_percentage
from methodAWS import process_images_in_folder
from postProcessVision import extract_course_info
from postProcessRegex import regex_post_process
from postProcessOSL import post_process_OSL
from methodVisionOSL import method_vision_osl
from huggingFaceMethod import hugging_method
from methodExtractTable import extractTable


def method_vision_ZSL(transcript_name, output_folder, orig):
    output_folder = output_folder + "ZSL"

    # STEP 1: Convert PDF to Folder of PNGs
    pdf_png_conversion(transcript_name, output_folder)
   
    #STEP 2: Run Vision or AWS on folder
    vision_ZSL(output_folder)

    #STEP 3: Concatenate all PNGs
    concatenate_csv_files(output_folder)

    #STEP 4: Find match percentage of pre-preprocess
    print(output_folder, "PRE PROCESS MATCH:")
    match_percentage(output_folder + '/' + output_folder + '_combined.csv', 'validation/'+ orig + '.csv')

    #STEP 5: Find match percentage for post-processed numbers
    post_process_method(output_folder ,orig)

def method_awsBoto(transcript_name, output_folder, orig):

    output_folder = output_folder + "awsBoto"
    # STEP 1: Convert PDF to Folder of PNGs
    pdf_png_conversion(transcript_name, output_folder)
    

    #STEP 2: Run Vision or AWS on folder
    process_images_in_folder(output_folder)
    

    #STEP 3: Concatenate all PNGs
    concatenate_csv_files(output_folder)

    #STEP 4: Find match percentage of pre-preprocess
    print(output_folder, "PRE PROCESS MATCH:")
    match_percentage(output_folder + '/' + output_folder + '_combined.csv', 'validation/'+ orig + '.csv')

    #STEP 5: Find match percentage for post-processed numbers
    post_process_method(output_folder ,orig)

def method_visioOSL(transcript_name, output_folder, orig):

    output_folder = output_folder + "OSL"
    # STEP 1: Convert PDF to Folder of PNGs
    pdf_png_conversion(transcript_name, output_folder)
   
    #STEP 2: Run Vision or AWS on folder
    
    method_vision_osl(output_folder, 'input_ex.png', 'output_ex.csv', orig)

    #STEP 3: Concatenate all PNGs
    concatenate_csv_files(output_folder)
     
    #STEP 4: Find match percentage of pre-preprocess
    print(output_folder, "PRE PROCESS MATCH:")
    match_percentage(output_folder + '/' + output_folder + '_combined.csv', 'validation/'+ orig + '.csv')

    #STEP 5: Find match percentage for post-processed numbers
    post_process_method(output_folder, orig)
def method_hugging(transcript_name, output_folder, orig):

    output_folder = output_folder
    # STEP 1: Convert PDF to Folder of PNGs
    pdf_png_conversion(transcript_name, output_folder)
   
    #STEP 2: Run Vision or AWS on folder
    
    hugging_method(output_folder)

    #STEP 3: Concatenate all PNGs
    concatenate_csv_files(output_folder)
     
    #STEP 4: Find match percentage of pre-preprocess
    print(output_folder, "PRE PROCESS MATCH:")
    match_percentage(output_folder + '/' + output_folder + '_combined.csv', 'validation/'+ orig + '.csv')

    #STEP 5: Find match percentage for post-processed numbers
    post_process_method(output_folder, orig)

def method_extractTable(transcript_name, output_folder, orig):

   

    output_folder = output_folder + "extractTable"
    # STEP 1: Convert PDF to Folder of PNGs
    # print("BROOOOOOOOOOOO")
    pdf_png_conversion(transcript_name, output_folder)
    api_key= "vi9070QHcjEfCXwa9AonTmwNQ1o5PTagfYJDXNNW"
    

    #STEP 2: Run Vision or AWS on folder
    extractTable(orig, api_key, output_folder)
    

    #STEP 3: Concatenate all PNGs
    concatenate_csv_files(output_folder)

   

    #STEP 4: Find match percentage of pre-preprocess
    print(output_folder, "PRE PROCESS MATCH:")
    match_percentage(output_folder + '/' + output_folder + '_combined.csv', 'validation/'+ orig + '.csv')

    #STEP 5: Find match percentage for post-processed numbers
    post_process_method(output_folder ,orig)

    
def post_process_method(output_folder, orig):

    print(output_folder, "open 4o ---------------------------------------------------------------------------")
    post_process_OSL('input_example.csv', 'output_example.csv', output_folder)
    match_percentage(output_folder + '/' +'Final_post_processed_gpt4o.csv', 'validation/'+ orig + '.csv')
    print(output_folder, "---------------------------------------------------------------------------")
    #REGEX SYSTEM
    regex_post_process(output_folder)
    # post_process_2 - open ai + regex
   
    print(output_folder, "regex ---------------------------------------------------------------------------")
    match_percentage(output_folder + '/' +'FINAL_post_process_REGEX.csv', 'validation/'+ orig + '.csv')
    print("---------------------------------------------------------------------------------------------")
    extract_course_info(output_folder)
    # post_process_2 - open ai + open ai
    
    print(output_folder, "OPEN AI  ---------------------------------------------------------------------------")
    match_percentage(output_folder + '/' +'FINAL_post_process_OPEN_AI.csv', 'validation/'+ orig + '.csv')
    print("---------------------------------------------------------------------------------------------")
    # FINAL_post_process_3 - open ai + open ai + regex
    
    print(output_folder, "OPEN AI  + regex")
    match_percentage(output_folder + '/' +'FINAL_post_process_COMBO.csv', 'validation/'+ orig + '.csv')
    print("---------------------------------------------------------------------------------------------")


output_folder = ['asu', 'dickonson_uni', 'edmonds', 'g_r', 'taylor','trans', 'uva', 'va', 'west_mich']
transcript_name = ['transcripts/asu', 'transcripts/dickonson_uni', 'transcripts/edmonds', 'transcripts/g_r', 'transcripts/taylor','transcripts/trans', 'transcripts/uva', 'transcripts/va', 'transcripts/west_mich']


for i in range(len(output_folder)):
    method_vision_ZSL(transcript_name[i], output_folder[i], output_folder[i])
    method_awsBoto(transcript_name[i], output_folder[i], output_folder[i])
    method_visioOSL(transcript_name[i], output_folder[i], output_folder[i])
    method_hugging(transcript_name[i], output_folder[i], output_folder[i])
    method_extractTable(transcript_name[i], output_folder[i], output_folder[i])

    #post(transcript_name[i], output_folder[i])