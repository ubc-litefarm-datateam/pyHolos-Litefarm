# # -----------------------------------------------------------#
# from data_loader.get_farm_data import FarmData
# from data_loader.get_modifers import Modifiers
# from data_loader.get_crop_group_params import CropGroupManager
# from data_loader.get_crop_params import CropParametersManager
# from data_loader.get_climate_params import ClimateDataExtractor

# farm_id = '0369f026-1f90-11ee-b788-0242ac150004'
# farm_data = FarmData(farm_id)
# print(farm_data.farm_data)

# group_params = CropGroupManager(farm_data)
# print(group_params.crop_group)
# print(group_params.crop_group_params)

# crop_params = CropParametersManager(farm_data)
# print(crop_params.crop_parameters)

# climate_params = ClimateDataExtractor(farm_data)
# climate_data = climate_params.extract_climate_data()
# print(climate_data)

# modifiers = Modifiers(farm_data, climate_data["soil_texture"])
# print(modifiers.modifiers)

# # -----------------------------------------------------------#
from data_loader.get_full_params import FarmDataManager
from crop_residue_calculator import CropResidueCalculator

farm_id = '0369f026-1f90-11ee-b788-0242ac150004'
farm_data_manager = FarmDataManager(farm_id)
all_data = farm_data_manager.gather_all_data()
print(all_data)

crop_residue = CropResidueCalculator(all_data)
print(crop_residue.above_ground_residue_n())