from data_loader.get_farm_data import FarmData
from data_loader.get_climate_params import ClimateDataManager
from data_loader.get_modifers import Modifiers
from data_loader.get_crop_group_params import CropGroupManager
from data_loader.get_crop_params import CropParametersManager

class FarmDataManager:
    def __init__(self, input_file, farm_id, mode = 'default'):
        # self.mode = mode
        self.farm_data = FarmData(input_file=input_file, farm_id=farm_id)
        self.climate_data_extractor = ClimateDataManager(self.farm_data, mode=mode)
        self.climate_data = self.climate_data_extractor.get_climate_data()
        self.modifiers = Modifiers(self.farm_data, self.climate_data['soil_texture'])
        self.crop_parameters_manager = CropParametersManager(self.farm_data, self.climate_data)
        self.crop_group_manager = CropGroupManager(self.farm_data)

    def gather_all_data(self):
        all_data = {
            'farm_data': self.farm_data.farm_data,
            'crop_group_params': self.crop_group_manager.crop_group_params,
            'crop_parameters': self.crop_parameters_manager.crop_parameters,
            'climate_data': self.climate_data,
            'modifiers': self.modifiers.modifiers
        }
        return all_data