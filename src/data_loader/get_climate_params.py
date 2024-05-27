import os
import numpy as np
import pandas as pd
import geopandas as gpd
from data_loader.get_external_climate_params import ExternalClimateDataFetcher
from data_loader.get_external_soil_params import ExternalSoilTextureDataFetcher
from data_loader.generate_random_points import generate_random_points, extract_lon_lat

class ClimateSoilDataManager:
    def __init__(self, farm_data, source='default', operation_mode='farmer', num_runs=5):
        self.farm_data = farm_data
        self.farm_point = (self.farm_data.farm_data['longitude'],
                           self.farm_data.farm_data['latitude'])
        self.start_year = self.farm_data.farm_data['start_year']
        self.end_year = self.farm_data.farm_data['end_year']
        self.source = source
        self.operation_mode = operation_mode
        self.num_runs = num_runs
        self.dir = os.path.dirname(__file__)
        # self.fetcher = None  # Initialize as None
        self.climate_soil_dict = None  # Initialize the climate data dictionary as None

    def load_climate_data(self):
        climate_path = os.path.join(
            self.dir, '../../data/raw/Holos/ecodistrict_to_ecozone_mapping.csv')
        return pd.read_csv(climate_path)
    
    def load_ecodistrict_polygons(self):
        ecodistrict_path = os.path.join(
            self.dir, '../../data/external/slc_dissolved_ecodistrict')
        ecodistrict = gpd.read_file(ecodistrict_path)
        return ecodistrict.to_crs('EPSG:4326')

    def extract_farm_ecoid_df(self):
        ecodistrict = self.load_ecodistrict_polygons()
        farm_ecoid_df = gpd.sjoin(self.farm_data.farm_gdf,
                                  ecodistrict[["ECO_ID", "geometry"]],
                                  how='left', 
                                  predicate='within').drop(columns=['index_right'])
        return farm_ecoid_df

    def extract_farm_ecodistrict_polygon(self):
        ecodistrict = self.load_ecodistrict_polygons()
        farm_ecodistrict = gpd.sjoin(ecodistrict,
                                     self.farm_data.farm_gdf,
                                     how='inner', 
                                     predicate='contains')
        return farm_ecodistrict["geometry"].iloc[0]
        
    def extract_default_climate_soil_data(self):
        farm_ecoid_df = self.extract_farm_ecoid_df()
        default_climate_df = self.load_climate_data()
 
        farm_ecoid_climate_soil = pd.merge(farm_ecoid_df, default_climate_df,
                                           how='left',
                                           left_on=['ECO_ID', 'province'],
                                           right_on=['Ecodistrict', 'Province'])
        
        farm_ecoid_climate_soil = farm_ecoid_climate_soil.drop(
            columns=['ECO_ID', 'Ecozone', 'province', 'SoilType'])

        self.climate_soil_dict = {
            "soil_texture": np.array([farm_ecoid_climate_soil["SoilTexture"].iloc[0].lower()]),
            "P": np.array([float(farm_ecoid_climate_soil["PMayToOct"].iloc[0])]),
            "PE": np.array([float(farm_ecoid_climate_soil["PEMayToOct"].iloc[0])]),
            "FR_Topo": farm_ecoid_climate_soil["Ftopo"].iloc[0],
            "locations": np.array([self.farm_point])
        }

    
    def get_climate_data(self):
        # if using `default` data source, operation_mode is default as `farmer`
        if self.source == 'default':
            self.extract_default_climate_soil_data()
            return self.climate_soil_dict

        # if using `exteranl` data source, operation_mode can be `farmer`, 
        # which returns location-specific soil and climate parameters
        # or `scientific`, which returns arrays of soild and climate parameters
        # based on farm-location and the randomly generated points within 
        # the corresponding ecodistrict
        if self.source == 'external' and self.operation_mode == 'farmer':
            # initialize the climate_soil_dict with default values
            self.extract_default_climate_soil_data()
            
            # get external soil texture
            external_soil_texture_fetcher = ExternalSoilTextureDataFetcher([self.farm_point, ])
            soil_result = external_soil_texture_fetcher.get_soil_texture()

            # get external climate data
            external_climate_data_fetcher = ExternalClimateDataFetcher(
                [self.farm_point,], self.start_year, self.end_year
            )
            climate_result = external_climate_data_fetcher.process_points_over_years()
            # Retrieve result for the specific point            
            climate_data = climate_result[self.farm_point]

            # Check if data retrieval was successful
            if climate_data['success']:
                # Append data if successfully fetched
                self.climate_soil_dict['P'] = np.array([climate_data['P']])
                self.climate_soil_dict['PE'] = np.array([climate_data['PE']])
                self.climate_soil_dict['soil_texture'] = np.array([soil_result[self.farm_point]])
                self.climate_soil_dict['locations'] = np.array([self.farm_point]) 
                return self.climate_soil_dict
            else:
                # On error or if data is unavailable, log the error and use default data
                print("Error in fetching or calculating precise P and PE. Using default.")
                return self.climate_soil_dict

        # if operation mode is scientific, then the data source must be 'external'
        if self.operation_mode == 'scientific':
            # initialize the climate_soil_dict with default values
            self.extract_default_climate_soil_data()

            # generate random points
            farm_ecodistrict_polygon = self.extract_farm_ecodistrict_polygon()
            random_points = generate_random_points(
                farm_ecodistrict_polygon, num_points=self.num_runs
            )
            points_list = extract_lon_lat(random_points)
            # attach the farm location lon & lat as the first element in the point list
            points_list.insert(0, self.farm_point)

            # Fetch climate data
            external_climate_data_fetcher = ExternalClimateDataFetcher(
                points_list, self.start_year, self.end_year)
            climate_results = external_climate_data_fetcher.process_points_over_years()

            # get external soil textrue data
            external_soil_texture_fetcher = ExternalSoilTextureDataFetcher(points_list)
            soil_results = external_soil_texture_fetcher.get_soil_texture()

            # Initialize lists for arrays
            points_array = []
            p_values = []
            pe_values = []
            soil_textures = []

            # Process each point in the list
            for point in points_list:
                points_array.append(point)  # always add the point
                climate_data = climate_results[point]

                # Check if data retrieval was successful
                if climate_data['success']:
                    # Append data if successfully fetched
                    p_values.append(climate_data['P'])
                    pe_values.append(climate_data['PE'])
                else:
                    # Append numpy.nan for P and PE if data fetching was unsuccessful
                    p_values.append(np.nan)
                    pe_values.append(np.nan)
                    print(f"Error fetching climate data for point {point}: {climate_data['error']}")

                # Retrieve soil texture data
                soil_textures.append(soil_results[point])

            
            # Convert lists to NumPy arrays
            self.climate_soil_dict['locations'] = np.array(points_array)
            self.climate_soil_dict['P'] = np.array(p_values)
            self.climate_soil_dict['PE'] = np.array(pe_values)
            self.climate_soil_dict['soil_texture'] = np.array(soil_textures)

            return self.climate_soil_dict 





