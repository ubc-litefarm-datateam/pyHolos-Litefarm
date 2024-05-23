import argparse
import json
import os
import numpy as np
from data_loader.get_full_params import FarmDataManager
from crop_residue_calculator import CropResidueCalculator
from emission_factor_calculator import EmissionFactorCalculator
from emission_calculator import EmissionCalculator

def main(farm_id, mode):
    farm_data_manager = FarmDataManager(farm_id, mode)
    all_data = farm_data_manager.gather_all_data()

    crop_resid = CropResidueCalculator(all_data)
    crop_residue = crop_resid.get_crop_residue()

    emission_factor_calc = EmissionFactorCalculator(all_data)
    emission_factor = emission_factor_calc.get_ef()

    emission_calc = EmissionCalculator(emission_factor, crop_residue)
    N_emission = emission_calc.get_emission()

    output = {
        'Input Parameters': all_data,
        'Crop Nitrogen Residue': crop_residue,
        'Emission Factors': emission_factor,
        'Total Direct Nitrogen Emission': N_emission
    }

    # Get the directory of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))
    output_path = os.path.join(dir_path, '..', 'outputs', 'output.json')

    # Write the JSON to the outputs folder
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=4)
        
def convert_numpy(data):
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
    parser.add_argument("--farm_id", type=str, required=True, help="Farm ID")
    parser.add_argument("--mode", type=str, default="default", choices=['default', 'precise'], help="Mode of data fetching")
    args = parser.parse_args()
    main(args.farm_id, args.mode)
