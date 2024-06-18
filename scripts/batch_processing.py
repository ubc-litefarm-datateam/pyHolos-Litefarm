"""
This module facilitates batch processing, specifically designed to execute sensitivity analyses 
for large-scale farm data for N2O emissions calculation. Users are encouraged to
modify and extend the functionality of this script to tailor it to their specific requirements.
The code provides a flexible framework for processing data in batches, handling errors,
and logging.

Feel free to adapt the batch size, error handling, and subprocess command configuration
to meet your specific operational needs.
"""

import pandas as pd
import subprocess
import os


def run_batch_process(input_csv, start_index=0, batch_size=3):
    """
    Process data in batches from a specified CSV file. This function manages the
    batch processing by iterating through rows in specified batch sizes, and logs progress
    or errors.

    Parameters
    ----------
    input_csv : str
        Relative path to the input CSV file containing the data.
    start_index : int, optional
        The starting index from which to begin processing, allowing for resumption of processing.
        Default is 0.
    batch_size : int, optional
        The number of rows to process in each batch. Default is 3.

    Returns
    -------
    None
        Outputs are handled by subprocess calls and potential error logging.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_py_path = os.path.join(script_dir, "../src/main.py")
    input_csv_path = os.path.join(script_dir, input_csv)
    # Load the farm information from CSV
    df = pd.read_csv(input_csv_path)

    for start in range(start_index, len(df), batch_size):
        batch_df = df[start : start + batch_size]
        try:
            process_batch(batch_df, main_py_path, input_csv_path)
            print(f"Successfully processed rows {start} to {start + len(batch_df) - 1}")
        except Exception as e:
            print(
                f"Error processing rows {start} to {start + len(batch_df) - 1}: {str(e)}"
            )
            error_index_path = os.path.join(script_dir, "error_index.txt")
            with open(error_index_path, "w") as f:
                f.write(str(start))  # Save the index of the start of the failed batch
            break  


def process_batch(batch_df, main_py_path, input_csv_path):
    """
    Executes a subprocess to run a Python script for each row in the batch dataframe.
    This function constructs the necessary command to execute the script with parameters
    taken from the dataframe.

    Parameters
    ----------
    batch_df : DataFrame
        A pandas DataFrame containing a batch of rows to be processed.
    main_py_path : str
        The absolute path to the 'main.py' script that will be executed.
    input_csv_path : str
        The absolute path to the input CSV file, which is passed as an argument to the script.

    Returns
    -------
    None
        Execution results are dependent on the 'main.py' script's outcomes; errors will
        raise an exception.
    """
    for index, row in batch_df.iterrows():
        farm_id = row["farm_id"]
        crop = row["common_crop_name"]
        # Define the output JSON file name based on farm_id and crop
        output_file = f"sensitivity_analysis/{farm_id}_{crop}.json"

        # Construct the command to run main.py
        command = [
            "python",
            main_py_path,
            "-i",
            input_csv_path,
            "--farm_id",
            farm_id,
            "--crop",
            crop,
            "--operation_mode",
            "scientific",
            "--source",
            "external",
            "--num_runs",
            "100",
            "-o",
            output_file,
        ]
        subprocess.run(command, check=True)


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_csv = "../data/test/LiteFarm_CA_HypotheticalFarmCropYields.csv"
    error_index_path = os.path.join(script_dir, "error_index.txt")
    try:
        with open(error_index_path, "r") as f:
            start_index = int(f.read().strip())  # Read the saved index
    except FileNotFoundError:
        start_index = 0  # No error file, start from the beginning

    run_batch_process(input_csv, start_index=start_index)
