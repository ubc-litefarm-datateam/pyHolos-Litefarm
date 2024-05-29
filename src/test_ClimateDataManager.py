from data_loader.get_farm_data import FarmData
from data_loader.get_climate_params import ClimateSoilDataManager
from data_loader.get_external_soil_params import ExternalSoilTextureDataFetcher

if __name__ == '__main__':    
    input_file = 'data/test/litefarm_test.csv'
    farm_id = '0369f026-1f90-11ee-b788-0242ac150004'
    farm_data = FarmData(input_file=input_file, farm_id=farm_id)
    print(farm_data.farm_data)
    
    # farm_point = (farm_data.farm_data['longitude'], farm_data.farm_data['latitude'])
    # print(farm_point)
    
    # external_soil_texture_fetcher = ExternalSoilTextureDataFetcher([farm_point])
    # soil_result = external_soil_texture_fetcher.get_soil_texture()
    # print(soil_result)
    
    climate_manager = ClimateSoilDataManager(farm_data, source='default') # operation_mode is default to 'farmer'
    climate_data = climate_manager.get_climate_data()
    print("Farmer's mode, get default P, PE, and soil texture ", climate_data)
    
    climate_manager2 = ClimateSoilDataManager(farm_data, source='external')  # operation_mode is default to 'farmer'
    climate_data2 = climate_manager2.get_climate_data()
    print("Farmer's mode, get external P, PE and soil texture: ", climate_data2)
    
    climate_manager3 = ClimateSoilDataManager(farm_data, source='external', operation_mode='scientific', num_runs=10)
    climate_data3 = climate_manager3.get_climate_data()
    print("Scientific mode, external P, PE and soil texture for 10 runs: ", climate_data3)

# climate_manager3 = ClimateDataManager(farm_data, source='external', operation_mode='scientific')
# climate_data3 = climate_manager3.get_climate_data()
# print("Get farm location specific P and PE, random points in ecodistrict: ", climate_data3)
