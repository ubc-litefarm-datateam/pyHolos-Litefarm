# # -----------------------------------------------------------#
# from data_loader.get_farm_data import FarmData
# from data_loader.get_climate_params import ClimateDataManager
# from data_loader.get_modifers import Modifiers
# from data_loader.get_crop_group_params import CropGroupManager
# from data_loader.get_crop_params import CropParametersManager


# farm_id = '0369f026-1f90-11ee-b788-0242ac150004'
# farm_data = FarmData(farm_id)
# print(farm_data.farm_data)

# climate_manager2 = ClimateDataManager(farm_data, mode='default')
# climate_data2 = climate_manager2.get_climate_data()
# print("Get ecodistrict P and PE: ", climate_data2)

# climate_manager = ClimateDataManager(farm_data, mode='precise')
# climate_data = climate_manager.get_climate_data()
# print("Get farm location specific P and PE: ", climate_data)

# modifiers = Modifiers(farm_data, climate_data["soil_texture"])
# print(modifiers.modifiers)

# crop_params = CropParametersManager(farm_data, climate_data)
# print(crop_params.crop_parameters)

# group_params = CropGroupManager(farm_data)
# print(group_params.crop_group)
# print(group_params.crop_group_params)

# # -----------------------------------------------------------#
# from data_loader.get_full_params import FarmDataManager
# from crop_residue_calculator import CropResidueCalculator
# from emission_factor_calculator import EmissionFactorCalculator
# from emission_calculator import EmissionCalculator

# farm_id = '0369f026-1f90-11ee-b788-0242ac150004'
# farm_data_manager = FarmDataManager(farm_id)
# all_data = farm_data_manager.gather_all_data()
# print('Default mode:', all_data)

# # farm_data_manager2 = FarmDataManager(farm_id)
# # all_data2 = farm_data_manager.gather_all_data()
# # print('Precise mode:', all_data2)

# crop_resid = CropResidueCalculator(all_data)
# crop_residue = crop_resid.get_crop_residue()
# print(crop_residue)

# emission_factor_calc = EmissionFactorCalculator(all_data)
# emission_factor = emission_factor_calc.get_ef()
# print(emission_factor)

# emission_calc = EmissionCalculator(emission_factor, crop_residue)
# N_emission = emission_calc.get_emission()
# print(N_emission)

# # -----------------------------------------------------------#
# from data_loader.get_external_climate_params import GrowingSeasonExternalDataFetcher

# # Example data
# latitude = 46.476
# longitude = -71.519
# year = 2021

# # Create an instance of the GrowingSeasonDataFetcher
# season_data_fetcher = GrowingSeasonExternalDataFetcher(latitude, longitude, year)

# # Fetch and calculate the total precipitation and evapotranspiration
# results = season_data_fetcher.calculate_growing_season_totals()

# # Check if the operation was successful and print results or handle errors
# if results and 'success' in results and results['success']:
#     print("Growing Season Data for Year 2021:")
#     print(f"Total Precipitation (mm): {results['data']['P']}")
#     print(f"Total Evapotranspiration (mm): {results['data']['PE']}")
# else:
#     error_message = results['error'] if 'error' in results else "Unknown error."
#     print(f"Failed to calculate growing season data. Error: {error_message}")

# # -----------------------------------------------------------#
# from data_loader.get_farm_data import FarmData
# from data_loader.get_climate_params import ClimateDataManager

# farm_id = '0369f026-1f90-11ee-b788-0242ac150004'
# farm_data = FarmData(farm_id)
# print(farm_data.farm_data)

# climate_manager2 = ClimateDataManager(farm_data, mode='default')
# climate_data2 = climate_manager2.get_climate_data()
# print("Get ecodistrict P and PE: ", climate_data2)

# climate_manager = ClimateDataManager(farm_data, mode='precise')
# climate_data = climate_manager.get_climate_data()
# print("Get farm location specific P and PE: ", climate_data)



