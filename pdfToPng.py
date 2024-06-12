import os
import glob, fitz


# This module is the first step to the system and converts the transcripts that are pdf to a folder containing the png versions
# transcript_name should be in the format: 'transcripts/[name of transcript]'


def pdf_png_conversion(transcript_name, output_folder):

    # To get better resolution
    zoom_x = 2.0  # horizontal zoom
    zoom_y = 2.0  # vertical zoom
    mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension

    all_files = glob.glob(transcript_name + "*.pdf")

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
   
    for filename in all_files:
        doc = fitz.open(filename)  # open document
        for page in doc:  # iterate through the pages
            pix = page.get_pixmap(matrix=mat)  # render page to an image
            output_path = os.path.join(output_folder, f"page-{page.number}.png")
            pix.save(output_path)
    print(transcript_name, "converted into a folder of pngs called: ", output_folder)


