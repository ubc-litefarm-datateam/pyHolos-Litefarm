import pandas as pd
import subprocess
import os

def run_batch_process(input_csv):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Path to main.py relative to the script location
    main_py_path = os.path.join(script_dir, '../src/main.py')
    # Correct the input CSV file path
    input_csv_path = os.path.join(script_dir, input_csv)
    # Load the farm information from CSV
    df = pd.read_csv(input_csv_path)
    
    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        farm_id = row['farm_id']
        crop = row['common_crop_name']
        # Define the output JSON file name based on farm_id and crop
        output_file = f"{farm_id}_{crop}.json"

        # Construct the command to run main.py
        command = [
            'python', main_py_path,
            '-i', input_csv_path, 
            '--farm_id', farm_id,
            '--crop', crop,
            '--operation_mode', 'scientific',
            '--source', 'external',
            '--num_runs', '5',
            '-o', output_file
        ]

        # Run the command
        try:
            subprocess.run(command, check=True)
            print(f"Processed {farm_id} for crop {crop}, results saved to {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to process {farm_id} for crop {crop}. Error: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred for {farm_id} with crop {crop}: {str(e)}")

if __name__ == '__main__':
    input_csv = '../data/test/litefarm_test.csv'
    run_batch_process(input_csv)
