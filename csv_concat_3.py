import os
import glob

def concatenate_csv_files(output_folder):
    # Path where the combined CSV file will be saved
    output_file_path = os.path.join(output_folder, output_folder + '_combined.csv')
    
    # Find all CSV files in the output folder
    csv_files = glob.glob(os.path.join(output_folder, '*.csv'))
    print("CSV Files Found:", csv_files)
    
    # Open the output file in write mode (this will create a new file or overwrite an existing file)
    with open(output_file_path, 'w') as outfile:
        first_file = True
        for file_path in csv_files:
            # Open each CSV file in read mode
            with open(file_path, 'r') as infile:
                # Skip the header of each file except the first one
                if first_file:
                    first_file = False
                else:
                    infile.readline()  # Skip the header line
                
                # Write the contents of the CSV file to the output file
                outfile.write(infile.read())
            
    
    print(f"All CSV files have been combined into: {output_file_path}")

# Call the function with the name of your folder containing CSV files
#concatenate_csv_files("trans")