import os
import sys
import json
import subprocess

def get_or_create_data_file():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dir_name = "sensitivity_analysis_sample_case"
    file_name = "farm_100_run_sci_mode.json"
    data_path = os.path.join(script_dir, '../../data/outputs', dir_name)
    rel_file_path = os.path.join(data_path, file_name)

    # Check if the directory and file exist
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    if not os.path.exists(rel_file_path):
        # Command to create the file if it does not exist
        command = "python src/main.py -i data/test/hypothetical_farm_data.csv --farm_id farm1 --crop Soybean --operation_mode scientific --source external --num_runs 100 -o " + rel_file_path
        subprocess.run(command, shell=True, check=True)

    # Load the JSON data if the file exists
    with open(rel_file_path, 'r') as file:
        json_data = json.load(file)

    return json_data

if __name__ == "__main__":
    get_or_create_data_file()
