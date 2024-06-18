import argparse
import json
import os
import numpy as np
from data_loader.get_full_params import FarmDataHub
from calculator.crop_residue_aggregator import CropResidueAggregator
from calculator.emission_factor_aggregator import EmissionFactorAggregator
from calculator.emission_aggregator import EmissionAggregator


class NumpyEncoder(json.JSONEncoder):
    """Custom encoder for numpy data types"""

    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def main(
    input_file,
    farm_id,
    crop,
    source="default",
    operation_mode="farmer",
    num_runs=10,
    sampl_modifier="default",
    sampl_crop="default",
    sampl_crop_group="default",
    output_file="output.json",
):
    """
    Main function to process parameters for calculation, analyze crop residue, calculate 
    emission factors, and aggregate emissions output, finally outputting the results as 
    a JSON file.

    Parameters
    ----------
    input_file : str
        Path to the input data file.
    farm_id : str
        Identifier for the farm.
    crop : str
        Name of the crop.
    source : str, optional
        Source of the data ('default' or 'external'). Default is 'default'.
    operation_mode : str, optional
        Mode of operation for data processing ('farmer' or 'scientific'). Default is 'farmer'.
    num_runs : int, optional
        Number of simulation runs. Default is 10.
    sampl_modifier : str, optional
        Type of sampling modifier. Default is 'default'.
    sampl_crop : str, optional
        Type of sampling crop. Default is 'default'.
    sampl_crop_group : str, optional
        Type of sampling crop group. Default is 'default'.
    output_file : str, optional
        Name of the output JSON file. Default is 'output.json'.

    Returns
    -------
    None
        This function does not return any value but writes results to a file.
    """
    farm_data_manager = FarmDataHub(
        input_file=input_file,
        farm_id=farm_id,
        crop=crop,
        source=source,
        operation_mode=operation_mode,
        num_runs=num_runs,
        sampl_modifier=sampl_modifier,
        sampl_crop=sampl_crop,
        sampl_crop_group=sampl_crop_group,
    )
    all_data = farm_data_manager.gather_all_data()
    # print(all_data)

    crop_resid = CropResidueAggregator(all_data, operation_mode=operation_mode)
    crop_residue = crop_resid.crop_analysis()
    # print(crop_residue)

    emission_factor_calc = EmissionFactorAggregator(
        all_data, operation_mode=operation_mode
    )
    emission_factor = emission_factor_calc.get_result()
    # print(emission_factor)

    emission_calc = EmissionAggregator(
        emission_factor, crop_residue, operation_mode=operation_mode
    )
    N_emission = emission_calc.get_result()
    # print(N_emission)

    output = {
        "Input Parameters": all_data,
        "Crop Nitrogen Residue": crop_residue,
        "Emission Factors": emission_factor,
        "Total Direct Nitrogen Emission": N_emission,
    }

    # Get the directory of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))
    output_path = os.path.join(dir_path, "..", "data/outputs", output_file)

    # Write the JSON to the outputs folder
    with open(output_path, "w") as f:
        json.dump(output, f, indent=4, cls=NumpyEncoder)


def convert_numpy(data):
    """
    Convert numpy data types to native Python types suitable for JSON serialization.

    Parameters
    ----------
    data : various
        The data that may include numpy types.

    Returns
    -------
    various
        Data converted to native Python types, recursively handled if it's a collection.
    """
    if isinstance(data, np.int64):
        return int(data)
    elif isinstance(data, (np.float64, float)):
        # Format float to 8 decimal places and convert back to float
        return float(f"{data:.8f}")
    elif isinstance(data, np.ndarray):
        return [convert_numpy(item) for item in data]
    elif isinstance(data, dict):
        return {k: convert_numpy(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_numpy(v) for v in data]
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate Nitrogen Emissions")
    parser.add_argument(
        "-i", "--input", type=str, required=True, help="Input file path is required"
    )
    parser.add_argument(
        "--farm_id", type=str, required=True, help="Farm ID is required"
    )
    parser.add_argument("--crop", type=str, required=True, help="Crop name is required")
    parser.add_argument(
        "--mode",
        type=str,
        default="default",
        choices=["default", "precise"],
        help="Mode of data fetching (default or precise)",
    )
    parser.add_argument(
        "-o", "--output", type=str, default="output.json", help="Output file name"
    )
    parser.add_argument(
        "--source",
        type=str,
        default="default",
        help="Data source type (default or external)",
    )
    parser.add_argument(
        "--operation_mode",
        type=str,
        default="farmer",
        choices=["farmer", "scientific"],
        help="Operation mode of the calculation",
    )
    parser.add_argument(
        "--num_runs", type=int, default=10, help="Number of simulation runs"
    )
    parser.add_argument(
        "--sampl_modifier", type=str, default="default", help="Sampling modifier type"
    )
    parser.add_argument(
        "--sampl_crop", type=str, default="default", help="Sampling crop type"
    )
    parser.add_argument(
        "--sampl_crop_group",
        type=str,
        default="default",
        help="Sampling crop group type",
    )

    args = parser.parse_args()
    main(
        args.input,
        args.farm_id,
        args.crop,
        args.source,
        args.operation_mode,
        args.num_runs,
        args.sampl_modifier,
        args.sampl_crop,
        args.sampl_crop_group,
        args.output,
    )
