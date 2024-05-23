import os
import pandas as pd
import geopandas as gpd
from data_loader.get_external_climate_params import GrowingSeasonExternalDataFetcher

class ClimateDataManager:
    def __init__(self, farm_data, mode='default'):
        self.farm_data = farm_data
        self.mode = mode
        self.dir = os.path.dirname(__file__)
        self.fetcher = None  # Initialize as None
        self.climate_dict = None  # Initialize the climate data dictionary as None

    def load_climate_data(self):
        climate_path = os.path.join(self.dir,
                                    '../../data/raw/Holos/ecodistrict_to_ecozone_mapping.csv')
        return pd.read_csv(climate_path)
    
    def load_slc_polygons(self):
        slc_polygons_path = os.path.join(self.dir, '../../data/external/slc')
        slc_polygons = gpd.read_file(slc_polygons_path)
        slc_polygons.set_crs('EPSG:4269', inplace=True)
        return slc_polygons.to_crs('EPSG:4326')
        
    def extract_default_climate_data(self):
        slc_polygons = self.load_slc_polygons()
        default_climate_df = self.load_climate_data()
        
        farm_polygons = gpd.sjoin(self.farm_data.farm_gdf, 
                                  slc_polygons[["POLY_ID", "ECO_ID", "geometry"]],
                                  how='left', 
                                  predicate='within').drop(columns=['index_right'])
        
        farm_ecodistrict_climate = pd.merge(farm_polygons, default_climate_df,
                                            how='left',
                                            left_on=['ECO_ID', 'province'],
                                            right_on=['Ecodistrict', 'Province'])
        
        farm_ecodistrict_climate = farm_ecodistrict_climate.drop(columns=['ECO_ID', 'Ecozone', 'province', 'SoilType'])

        self.climate_dict = {
            "soil_texture": farm_ecodistrict_climate["SoilTexture"].iloc[0].lower(),
            "P": farm_ecodistrict_climate["PMayToOct"].iloc[0],
            "PE": farm_ecodistrict_climate["PEMayToOct"].iloc[0],
            "FR_Topo": farm_ecodistrict_climate["Ftopo"].iloc[0]
        }

    def initialize_fetcher(self):
        # location = self.farm_data.farm_data['location'][0]
        # self.latitude = self.farm_data.farm_data['latitude']
        # self.longitude = self.farm_data.farm_data['longitude']
        year = self.farm_data.farm_data['year']
        self.fetcher = GrowingSeasonExternalDataFetcher(self.farm_data.farm_data['latitude'], 
                                                        self.farm_data.farm_data['longitude'], 
                                                        year)

    def get_climate_data(self):
        if self.mode == 'default':
            self.extract_default_climate_data()
            return self.climate_dict

        # Initialize fetcher if not already done and in 'precise' mode
        if self.fetcher is None:
            self.initialize_fetcher()

        result = self.fetcher.calculate_growing_season_totals()
        if result and 'success' in result and result['success']:
            # Replace P and PE with calculated values while keeping other data
            self.extract_default_climate_data()
            self.climate_dict['P'] = result['data']['P']
            self.climate_dict['PE'] = result['data']['PE']
            return self.climate_dict

        # On error or in any other case, return default data
        print("Error fetching or calculating precise data. Using default data.")
        self.extract_default_climate_data()
        return self.climate_dict



