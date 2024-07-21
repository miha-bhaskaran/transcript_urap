import pandas as pd
import os
from ExtractTable import ExtractTable

print(ExtractTable.VERSION)

api_key = "Fg4p08t4MNzX7T42w0RbYV2EAvdZQLEcRjqoCsBa"
et_sess = ExtractTable(api_key)
usage = et_sess.check_usage()

print(usage)
 
image_location = "taylor/page-5.png"

table_data = et_sess.process_file(filepath=image_location, output_format="df")


for index, table in enumerate(table_data):
    print(f"Table {index + 1}:")
    print(table)

# check if the folder exists
os.makedirs('taylor', exist_ok=True)

output_csv_location = "taylor/taylor_extractedTable.csv"
accumulate_all_dfs = pd.DataFrame()


accumulate_all_dfs = pd.concat(table_data, ignore_index=True)

print("Shape of all tables accumulated together is", accumulate_all_dfs.shape)

# Save the accumulated output to a CSV file
accumulate_all_dfs.to_csv(output_csv_location, index=False, header=True)

print(f"All tables saved to {output_csv_location}")