from pdf_png_1 import pdfPngConverter
from vision_script_2 import vision
from csv_concat_3 import concatenate_csv_files
from preProcess_4 import find_matching_lines

output_folder = 'trans'
transcript_name = 'transcripts/trans'

# STEP 1: Convert PDF to Folder of PNGs
pdfPngConverter(transcript_name, output_folder)

#STEP 2: Run Vision or AWS on folder
vision(output_folder)

#STEP 3: Concatenate all PNGs
concatenate_csv_files(output_folder)

#STEP 4: Find match percentage of pre-preprocess
find_matching_lines(output_folder + '/' + output_folder + '_combined.csv', 'validation/'+ output_folder + '.csv')

#STEP 5: Find match percentage for post-processed numbers

#REGEX

#Open AI
