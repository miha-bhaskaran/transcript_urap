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
from methodClaude import methodClaude
from methodO1 import methodO1


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
    match_percentage(output_folder + '/' + output_folder + '_combined.csv', 'testing_validation/'+ orig + '.csv')

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
    match_percentage(output_folder + '/' + output_folder + '_combined.csv', 'testing_validation/'+ orig + '.csv')

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
    match_percentage(output_folder + '/' + output_folder + '_combined.csv', 'testing_validation/'+ orig + '.csv')

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
    match_percentage(output_folder + '/' + output_folder + '_combined.csv', 'testing_validation/'+ orig + '.csv')

    #STEP 5: Find match percentage for post-processed numbers
    post_process_method(output_folder, orig)

def method_extractTable(transcript_name, output_folder, orig):

   
    output_folder = output_folder + "extractTable"
    # STEP 1: Convert PDF to Folder of PNGs
   
    pdf_png_conversion(transcript_name, output_folder)
    api_key= "86L2cv3UrotyBzUdpGFXHUC0ql12cqq4qiJG1awX"
    

    #STEP 2: Run Vision or AWS on folder
    extractTable(output_folder, api_key, output_folder)

    

    #STEP 3: Concatenate all PNGs
    concatenate_csv_files(output_folder)

   

    #STEP 4: Find match percentage of pre-preprocess
    print(output_folder, "PRE PROCESS MATCH:")
    match_percentage(output_folder + '/' + output_folder + '_combined.csv', 'testing_validation/'+ orig + '.csv')

    #STEP 5: Find match percentage for post-processed numbers
    post_process_method(output_folder ,orig)


# HERE

def method_claude(transcript_name, output_folder, orig):

   
    output_folder = output_folder + "claude"
    # STEP 1: Convert PDF to Folder of PNGs
   
    pdf_png_conversion(transcript_name, output_folder)
    api_key= "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"
    
    #STEP 2: Run claude
    methodClaude(output_folder, api_key, output_folder)

    

    #STEP 3: Concatenate all PNGs
    concatenate_csv_files(output_folder)

   

    #STEP 4: Find match percentage of pre-preprocess
    print(output_folder, "PRE PROCESS MATCH:")
    match_percentage(output_folder + '/' + output_folder + '_combined.csv', 'testing_validation/'+ orig + '.csv')

    # #STEP 5: Find match percentage for post-processed numbers
    post_process_method(output_folder ,orig)

def method_o1(transcript_name, output_folder, orig):

   
    output_folder = output_folder + "o1"
    # STEP 1: Convert PDF to Folder of PNGs
   
    pdf_png_conversion(transcript_name, output_folder)
    api_key= "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"
    
    #STEP 2: Run claude
    methodO1(output_folder, api_key, output_folder)

    

    #STEP 3: Concatenate all PNGs
    concatenate_csv_files(output_folder)

   

    #STEP 4: Find match percentage of pre-preprocess
    print(output_folder, "PRE PROCESS MATCH:")
    match_percentage(output_folder + '/' + output_folder + '_combined.csv', 'testing_validation/'+ orig + '.csv')

    # #STEP 5: Find match percentage for post-processed numbers
    #post_process_method(output_folder ,orig)
    
def post_process_method(output_folder, orig):

    #REGEX SYSTEM
    regex_post_process(output_folder)
    # post_process_2 - open ai + regex
    print(output_folder, "regex ---------------------------------------------------------------------------")
    match_percentage(output_folder + '/' +'FINAL_post_process_REGEX.csv', 'testing_validation/'+ orig + '.csv')
    print("---------------------------------------------------------------------------------------------")
   
    #ZSL
    extract_course_info(output_folder)
    # post_process_2 - open ai + open ai
    print(output_folder, "OPEN AI  ---------------------------------------------------------------------------")
    match_percentage(output_folder + '/' +'FINAL_post_process_OPEN_AI.csv', 'testing_validation/'+ orig + '.csv')
    print("---------------------------------------------------------------------------------------------")
    # FINAL_post_process_3 - open ai + open ai + regex
    
    #COMBO
    print(output_folder, "OPEN AI  + regex")
    match_percentage(output_folder + '/' +'FINAL_post_process_COMBO.csv', 'testing_validation/'+ orig + '.csv')
    print("---------------------------------------------------------------------------------------------")
    
    #OSL
    print(output_folder, "open 4o OSL ---------------------------------------------------------------------------")
    post_process_OSL('input_example.csv', 'output_example.csv', output_folder)
    match_percentage(output_folder + '/' +'Final_post_processed_gpt4o.csv', 'testing_validation/'+ orig + '.csv')
    print(output_folder, "---------------------------------------------------------------------------")
 

# output_folder = ['asu', 'dickonson_uni', 'edmonds', 'g_r', 'taylor','trans', 'uva', 'va', 'west_mich']
# transcript_name = ['transcripts/asu', 'transcripts/dickonson_uni', 'transcripts/edmonds', 'transcripts/g_r', 'transcripts/taylor','transcripts/trans', 'transcripts/uva', 'transcripts/va', 'transcripts/west_mich']



# output_folder = ['depaul', 'mich_state_uni', 'suny', 'kutztown_upenn', 'wayne','western_mich_uni']
# transcript_name = ['testing_transcripts/depaul', 'testing_transcripts/mich_state_uni', 'testing_transcripts/suny', 'testing_transcripts/kutztown_upenn', 'testing_transcripts/wayne','testing_transcripts/western_mich_uni']

# output_folder = ['wayne']
# transcript_name = ['testing_transcripts/wayne']

output_folder = ['herkimer_SUNY']
transcript_name = ['testing_transcripts/herkimer_SUNY']


#testing


for i in range(len(output_folder)):
    
    method_awsBoto(transcript_name[i], output_folder[i], output_folder[i])
    #method_visioOSL(transcript_name[i], output_folder[i], output_folder[i])
    method_o1(transcript_name[i], output_folder[i], output_folder[i])
    method_claude(transcript_name[i], output_folder[i], output_folder[i])
    # method_hugging(transcript_name[i], output_folder[i], output_folder[i])
             
    # method_extractTable(transcript_name[i], output_folder[i], output_folder[i])
    #method_claude(transcript_name[i], output_folder[i], output_folder[i])


    #post(transcript_name[i], output_folder[i])