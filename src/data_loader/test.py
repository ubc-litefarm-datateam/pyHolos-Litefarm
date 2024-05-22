# # -----------------------------------------------------------#
# from get_farm_data import FarmData
# from get_modifers import Modifiers
# from get_crop_group_params import CropGroupManager
# from get_crop_params import CropParametersManager
# from get_climate_params import ClimateDataExtractor

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
from get_full_params import FarmDataManager

farm_id = '0369f026-1f90-11ee-b788-0242ac150004'
farm_data_manager = FarmDataManager(farm_id)
all_data = farm_data_manager.gather_all_data()
print(all_data)

#-----------------------------------------------------------#
# from evapotranspiration_calculator import EvapotranspirationCalculator

# calculator = EvapotranspirationCalculator(20, 5, 45)
# et = calculator.calculate()
# print(f"Reference Evapotranspiration: {et} mm/day")
