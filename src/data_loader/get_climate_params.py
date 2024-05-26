import os
import numpy as np
import pandas as pd
import geopandas as gpd
from data_loader.get_external_climate_params import GrowingSeasonExternalDataFetcher
from data_loader.generate_random_points import generate_random_points, extract_lon_lat

class ClimateDataManager:
    def __init__(self, farm_data, source='default', operation_mode='farmer', num_runs=5):
        self.farm_data = farm_data
        self.source = source
        self.operation_mode = operation_mode
        self.num_runs = num_runs
        self.dir = os.path.dirname(__file__)
        # self.fetcher = None  # Initialize as None
        self.climate_dict = None  # Initialize the climate data dictionary as None

    def load_climate_data(self):
        climate_path = os.path.join(self.dir,
                                    '../../data/raw/Holos/ecodistrict_to_ecozone_mapping.csv')
        return pd.read_csv(climate_path)
    
    def load_ecodistrict_polygons(self):
        ecodistrict_path = os.path.join(self.dir, 
                                        '../../data/external/slc_dissolved_ecodistrict')
        ecodistrict = gpd.read_file(ecodistrict_path)
        return ecodistrict.to_crs('EPSG:4326')

    def extract_farm_ecodistrict(self):
        ecodistrict = self.load_ecodistrict_polygons()
        farm_polygons = gpd.sjoin(self.farm_data.farm_gdf,
                                  ecodistrict[["ECO_ID", "geometry"]],
                                  how='left', 
                                  predicate='within').drop(columns=['index_right'])
        return farm_polygons

    def extract_farm_ecodistrict_polygon(self):
        ecodistrict = self.load_ecodistrict_polygons()
        farm_ecodistrict = gpd.sjoin(ecodistrict,
                                     self.farm_data.farm_gdf,
                                     how='inner', 
                                     predicate='contains')
        return farm_ecodistrict["geometry"].iloc[0]
        
    def extract_default_climate_data(self):
        farm_polygons = self.extract_farm_ecodistrict()
        default_climate_df = self.load_climate_data()
 
        farm_ecodistrict_climate = pd.merge(farm_polygons, default_climate_df,
                                            how='left',
                                            left_on=['ECO_ID', 'province'],
                                            right_on=['Ecodistrict', 'Province'])
        
        farm_ecodistrict_climate = farm_ecodistrict_climate.drop(
            columns=['ECO_ID', 'Ecozone', 'province', 'SoilType'])

        self.climate_dict = {
            "soil_texture": farm_ecodistrict_climate["SoilTexture"].iloc[0].lower(),
            "P": float(farm_ecodistrict_climate["PMayToOct"].iloc[0]),
            "PE": float(farm_ecodistrict_climate["PEMayToOct"].iloc[0]),
            "FR_Topo": farm_ecodistrict_climate["Ftopo"].iloc[0]
        }

    # def cliamte_fetcher(self, latitude, longitude):
    #     year = self.farm_data.farm_data['year']
    #     self.fetcher = GrowingSeasonExternalDataFetcher(latitude, 
    #                                                     longitude, 
    #                                                     year)

    def get_climate_data(self):
        if self.source == 'default':
            self.extract_default_climate_data()
            return self.climate_dict

        # Initialize fetcher if not already done and in 'precise' mode
        if self.source == 'external' and self.operation_mode == 'farmer':
            external_climate_data_fetcher = GrowingSeasonExternalDataFetcher(
                self.farm_data.farm_data['latitude'], 
                self.farm_data.farm_data['longitude'], 
                self.farm_data.farm_data['year']
            )
            result = external_climate_data_fetcher.calculate_growing_season_totals()
            
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


        if self.operation_mode == 'scientific':
            P = np.array([])
            PE = np.array([])
            lons = np.array([])
            lats = np.array([])
            
            farm_ecodistrict_polygon = self.extract_farm_ecodistrict_polygon()
            random_points = generate_random_points(farm_ecodistrict_polygon, num_points=self.num_runs)
            points_coords = extract_lon_lat(random_points)

            for point in points_coords:
                longitude, latitude = point
                external_climate_data_fetcher = GrowingSeasonExternalDataFetcher(latitude,
                                                                                 longitude, 
                                                                                 self.farm_data.farm_data['year'])
                result = external_climate_data_fetcher.calculate_growing_season_totals()

                if result and 'success' in result and result['success']:
                    # Replace P and PE with calculated values while keeping other data
                    P = np.append(P, result['data']['P'])
                    PE = np.append(PE, result['data']['PE'])
                    lons = np.append(lons, longitude)
                    lats = np.append(lats, latitude)
                else:    
                    print("Error fetching or calculating precise data for random points. Using default data.")
                    self.extract_default_climate_data()
                    return self.climate_dict
                
            self.extract_default_climate_data()
            self.climate_dict['P'] = P
            self.climate_dict['PE'] = PE
            self.climate_dict['latitude'] = lats
            self.climate_dict['longitude'] = lons

            return self.climate_dict 
                         



