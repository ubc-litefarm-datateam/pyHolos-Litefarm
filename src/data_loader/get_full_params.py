import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_loader.get_farm_data import FarmData
from data_loader.get_climate_params import ClimateSoilDataManager
from data_loader.get_modifers import Modifiers
from data_loader.get_crop_group_params import CropGroupManager
from data_loader.get_crop_params import CropParametersManager

class FarmDataManager:
    def __init__(self, input_file, farm_id, source='default', operation_mode='farmer', num_runs=10):
        self.input_file = input_file
        self.farm_id = farm_id
        self.source = source
        self.operation_mode = operation_mode
        self.num_runs = num_runs

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

            all_data = {
                'farm_data': farm_data,
                'crop_group_params': crop_group_params, 
                'crop_parameters': crop_params,
                'climate_data': climate_data,
                'modifiers': modifiers
            }
        return all_data
    
# Example usage
if __name__ == '__main__':
    input_file = 'data/test/litefarm_test.csv'
    farm_id = '0369f026-1f90-11ee-b788-0242ac150004'
    farm_params = FarmDataManager(input_file=input_file, farm_id=farm_id)
    print(farm_params.gather_all_data())