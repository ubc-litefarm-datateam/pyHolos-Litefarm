import sys
import os
import json
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_loader.get_farm_data import FarmData
from data_loader.get_climate_params import ClimateSoilDataManager
from data_loader.get_modifers import Modifiers
from data_loader.get_crop_group_params import CropGroupManager
from data_loader.get_crop_params import CropParametersManager

class FarmDataManager:
    def __init__(self, input_file, farm_id, source='default', operation_mode='farmer', num_runs=10,
                 sampl_modifier='default', sampl_crop='default', sampl_crop_group='default'):
        self.input_file = input_file
        self.farm_id = farm_id
        self.source = source
        self.operation_mode = operation_mode
        self.num_runs = num_runs
        self.sampl_modifier = sampl_modifier
        self.sampl_crop = sampl_crop
        self.sampl_crop_group = sampl_crop_group

    def gather_all_data(self):
        farm = FarmData(input_file=self.input_file, farm_id=self.farm_id)
        farm_data = farm.farm_data

        if self.source == 'default':
            climate_data_extractor = ClimateSoilDataManager(
                farm, source=self.source,
            )
            climate_data = climate_data_extractor.get_climate_data()
            modifiers_manager = Modifiers(farm_data)
            modifiers = modifiers_manager.modifiers
            crop_parameters_manager = CropParametersManager(farm_data, climate_data)
            crop_params = crop_parameters_manager.crop_parameters
            crop_group_manager = CropGroupManager(farm_data)
            crop_group_params = crop_group_manager.crop_group_params

            all_params = {
                'farm_data': {k: np.array([v]) for k, v in farm_data.items()}, 
                # 'farm_data': farm_data,
                'crop_group_params': crop_group_params, 
                'crop_parameters': crop_params,
                'climate_data': climate_data,
                'modifiers': modifiers
            }
            return all_params
        
        elif self.source == 'external' and self.operation_mode=='farmer':
            climate_data_extractor = ClimateSoilDataManager(
                farm, source=self.source, operation_mode=self.operation_mode
            )
            climate_data = climate_data_extractor.get_climate_data()
            modifiers_manager = Modifiers(farm_data)
            modifiers = modifiers_manager.modifiers
            crop_parameters_manager = CropParametersManager(farm_data, climate_data)
            crop_params = crop_parameters_manager.crop_parameters
            crop_group_manager = CropGroupManager(farm_data)
            crop_group_params = crop_group_manager.crop_group_params

            all_params = {
                'farm_data': {k: np.array([v]) for k, v in farm_data.items()}, 
                'crop_group_params': crop_group_params, 
                'crop_parameters': crop_params,
                'climate_data': climate_data,
                'modifiers': modifiers
            }
            return all_params
        
        elif self.source == 'external' and self.operation_mode=='scientific':
            climate_data_extractor = ClimateSoilDataManager(
                farm, source=self.source, operation_mode=self.operation_mode, num_runs=self.num_runs
                )
            climate_data = climate_data_extractor.get_climate_data()

            modifiers_manager = Modifiers(farm_data)
            modifiers = modifiers_manager.sample_modifiers(
                sampling_mode=self.sampl_modifier, num_samples=self.num_runs
                )
            
            crop_parameters_manager = CropParametersManager(farm_data, climate_data)
            crop_params = crop_parameters_manager.sample_crop_parameters(
                sampling_mode=self.sampl_crop, num_samples=self.num_runs
            )
            
            crop_group_manager = CropGroupManager(farm_data)
            crop_group_params = crop_group_manager.sample_crop_group_parameters(
                sampling_mode=self.sampl_crop_group, num_samples=self.num_runs)
            
            all_params = {
                'farm_data': {k: np.array([v]) for k, v in farm_data.items()}, 
                'crop_group_params': crop_group_params, 
                'crop_parameters': crop_params,
                'climate_data': climate_data,
                'modifiers': modifiers
            }
            return all_params

        else:
            raise ValueError("Scientific mode cannot be run. Excution Halted.")

# Example usage
if __name__ == '__main__':
    input_file = 'data/test/litefarm_test.csv'
    farm_id = '0369f026-1f90-11ee-b788-0242ac150004'
    farm_params = FarmDataManager(
        input_file=input_file, farm_id=farm_id, source='default', operation_mode='farmer'
        )
    farmer_holos_default_params = farm_params.gather_all_data()
    print("Farmer's mode with Holos default data:", farmer_holos_default_params)

    farm_params2 = FarmDataManager(
        input_file=input_file, farm_id=farm_id, source='external', operation_mode='farmer'
        )
    farmer_external_params = farm_params2.gather_all_data()
    print("Farmer's mode with external climate & soil data:", farmer_external_params)

    farm_params3 = FarmDataManager(
        input_file=input_file, farm_id=farm_id, source='external', operation_mode='scientific'
        )
    scientific_params = farm_params3.gather_all_data()
    print("Scientific mode:", scientific_params)

    files = {
    'farmer_holos_default_params': farmer_holos_default_params,
    'farmer_external_params': farmer_external_params,
    'scientific_params': scientific_params
    }

    class NumpyEncoder(json.JSONEncoder):
        """ Custom encoder for numpy data types """
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return json.JSONEncoder.default(self, obj)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    for key, params in files.items():
        output_file = f'{key}.json'  # This will create filenames based on the keys
        output_path = os.path.join(dir_path, '..', '..', 'data', 'temp', output_file)

        # Write the JSON data to the file
        with open(output_path, 'w') as f:
            json.dump(params, f, indent=4, cls=NumpyEncoder)

        print(f"Saved {key} to {output_path}")