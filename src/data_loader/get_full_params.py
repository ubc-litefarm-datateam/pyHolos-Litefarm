from get_farm_data import FarmData
from get_modifers import Modifiers
from get_crop_group_params import CropGroupManager
from get_crop_params import CropParametersManager
from get_climate_params import ClimateDataExtractor

class FarmDataManager:
    def __init__(self, farm_id):
        self.farm_id = farm_id
        self.farm_data = FarmData(farm_id)
        self.climate_data_extractor = ClimateDataExtractor(self.farm_data)
        self.climate_data = self.climate_data_extractor.extract_climate_data()
        self.modifiers = Modifiers(self.farm_data, self.climate_data['soil_texture'])
        self.crop_group_manager = CropGroupManager(self.farm_data)
        self.crop_parameters_manager = CropParametersManager(self.farm_data)

    def gather_all_data(self):
        all_data = {
            'farm_data': self.farm_data.farm_data,
            'crop_group_params': self.crop_group_manager.crop_group_params,
            'crop_parameters': self.crop_parameters_manager.crop_parameters,
            'climate_data': self.climate_data,
            'modifiers': self.modifiers.modifiers
        }
        return all_data