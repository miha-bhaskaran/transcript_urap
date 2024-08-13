import pandas as pd
import os
from ExtractTable import ExtractTable

def extractTable(folder_path, api_key, output_folder):
    """
    Extracts tables from images in the specified folder and saves them as CSV files.

    Parameters:
    - folder_path: str, the path to the folder containing the images.
    - api_key: str, API key for the ExtractTable service.
    - output_folder: str, the path to the folder where CSV files will be saved.

    Output:
    - CSV files for each image with extracted tables.
    """

    # Initialize the ExtractTable session
    et_sess = ExtractTable(api_key)

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # List all files in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.png'):
            image_path = os.path.join(folder_path, filename)
            csv_filename = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.csv")

            # Extract table data from the image
            table_data = et_sess.process_file(filepath=image_path, output_format="df")

            # Accumulate all tables in a single DataFrame
            accumulate_all_dfs = pd.concat(table_data, ignore_index=True)

            print(f"Shape of all tables accumulated together from {filename} is", accumulate_all_dfs.shape)

            # Save the accumulated output to a CSV file
            accumulate_all_dfs.to_csv(csv_filename, index=False, header=True)
            print(f"Extracted tables from {filename} have been saved to {csv_filename}")
