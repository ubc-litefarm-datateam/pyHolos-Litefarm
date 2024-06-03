import pandas as pd
import subprocess
import os

def run_batch_process(input_csv, start_index=0, batch_size=3):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Path to main.py relative to the script location
    main_py_path = os.path.join(script_dir, '../src/main.py')
    # Correct the input CSV file path
    input_csv_path = os.path.join(script_dir, input_csv)
    # Load the farm information from CSV
    df = pd.read_csv(input_csv_path)

    for start in range(start_index, len(df), batch_size):
        batch_df = df[start:start+batch_size]
        try:
            process_batch(batch_df, main_py_path, input_csv_path)
            print(f"Successfully processed rows {start} to {start + len(batch_df) - 1}")
        except Exception as e:
            print(f"Error processing rows {start} to {start + len(batch_df) - 1}: {str(e)}")
            error_index_path = os.path.join(script_dir, 'error_index.txt')
            with open(error_index_path, 'w') as f:
                f.write(str(start)) # Save the index of the start of the failed batch
            break  # Optional: stop processing further on error
    
def process_batch(batch_df, main_py_path, input_csv_path):
    for index, row in batch_df.iterrows():
        farm_id = row['farm_id']
        crop = row['common_crop_name']
        # Define the output JSON file name based on farm_id and crop
        output_file = f"sensitivity_analysis/{farm_id}_{crop}.json"

        # Construct the command to run main.py
        command = [
            'python', main_py_path,
            '-i', input_csv_path, 
            '--farm_id', farm_id,
            '--crop', crop,
            '--operation_mode', 'scientific',
            '--source', 'external',
            '--num_runs', '100',
            '-o', output_file
        ]
        subprocess.run(command, check=True)

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_csv = '../data/test/LiteFarm_CA_HypotheticalFarmCropYields.csv'
    error_index_path = os.path.join(script_dir, 'error_index.txt')
    try:
        with open(error_index_path, 'r') as f:
            start_index = int(f.read().strip())  # Read the saved index
    except FileNotFoundError:
        start_index = 0  # No error file, start from the beginning
    
    run_batch_process(input_csv, start_index=start_index)
