import os
import glob

def concatenate_csv_files(output_folder):
    output_file_path = os.path.join(output_folder, output_folder + '_combined.csv')
    
   
    csv_files = glob.glob(os.path.join(output_folder, '*.csv'))
    print("CSV Files Found:", csv_files)
    
    with open(output_file_path, 'w') as outfile:
        first_file = True
        for file_path in csv_files:
            with open(file_path, 'r') as infile:
                if first_file:
                    first_file = False
                else:
                    infile.readline()  
                outfile.write(infile.read())
            
    
    print(f"All CSV files have been combined into: {output_file_path}")

