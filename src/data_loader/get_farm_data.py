import os
import json
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from datetime import datetime

class FarmData:
    def __init__(self, input_file, farm_id, crop):
        self.farm_id = farm_id
        self.crop = crop
        self.dir = os.path.dirname(__file__)
        self.input_file_path = os.path.join(self.dir, '..', '..', input_file)
        # self.province = None
        self.crop_to_group_map_path = os.path.join(
            self.dir, '../../data/preprocessed/crop_to_group.csv'
            )
        self.farm_data = self.get_farm_data()
        self.farm_gdf = self.get_farm_gdf()
        self.province = self.get_province()
        self.crop_group = self.get_crop_group()
        self.update_farm_dict()

    def get_farm_data(self):
        file_extension = os.path.splitext(self.input_file_path)[1]
        if file_extension == '.csv':
            df = pd.read_csv(self.input_file_path)
            df = df.query(f"farm_id == '{self.farm_id}' and common_crop_name == '{self.crop}'").copy()
            if df.empty:
                raise ValueError(f"No farm data found for farm_id {self.farm_id} with crop {self.crop}")
        elif file_extension == '.json':
            with open(self.input_file_path, 'r') as file:
                data = json.load(file)
                if self.farm_id in data:
                    df = pd.DataFrame([data[self.farm_id]])
                else:
                    raise ValueError(f"No farm data found for farm_id {self.farm_id}")
        else:
            raise ValueError("Unsupported file format")

        df.loc[:, 'area_in_m2'] = df['area_in_m2'].astype(float).map(lambda x: x * 0.0001)  # Convert and scale area
        df.loc[:, 'yield_kg_per_m2'] = df['yield_kg_per_m2'].astype(float).map(lambda x: x * 10000)  # Convert and scale yield
        df.loc[:, 'start_year'] = df['start_year'].astype(int)  # Ensure year is an integer
        df.loc[:, 'end_year'] = df['end_year'].astype(int)

        farm = df.iloc[0].to_dict()

        farm['area'] = float(farm['area_in_m2'])
        farm['yield'] = float(farm['yield_kg_per_m2'])
        farm['start_year'] = int(farm['start_year'])
        farm['end_year'] = int(farm['end_year'])
        
        farm_dict = {
            'farm_id' : self.farm_id,
            'area': farm['area'],
            'latitude': float(farm['latitude']),
            'longitude': float(farm['longitude']),
            'crop': farm['common_crop_name'],
            'yield': farm['yield'],
            'start_year': farm['start_year'],
            'end_year': farm['end_year']
        }

        self.farm_data = farm_dict 
        self.validate_data()
        return self.farm_data

    def get_farm_gdf(self):
        # Convert single values to lists if necessary
        if isinstance(self.farm_data['longitude'], (int, float)):
            longitudes = [self.farm_data['longitude']]
            latitudes = [self.farm_data['latitude']]
        else:
            longitudes = self.farm_data['longitude']
            latitudes = self.farm_data['latitude']
        
        locations = [Point(x, y) for x, y in zip(longitudes, latitudes)]
        farm_point = gpd.GeoDataFrame({'geometry': locations}, crs="EPSG:4326")
        province_shp_path = os.path.join(self.dir, '../../data/external/province_100m')
        provinces = gpd.read_file(province_shp_path).to_crs("EPSG:4326")
        farm_province = gpd.sjoin(farm_point, provinces[["PRENAME", "geometry"]],
                                  how='left', predicate='within').drop(columns=['index_right'])
        
        farm_province.rename(columns={'PRENAME': 'province'}, inplace=True)
        return farm_province

    def get_province(self):
        province = self.farm_gdf["province"].iloc[0]
        if province is None:
            raise ValueError("Selected location is not in Canada, select a new location in Canada")
        return province
    
    def get_crop_group(self):
        crop_to_group_map_df = pd.read_csv(self.crop_to_group_map_path)
        crop_group = crop_to_group_map_df.query(f"crop == '{self.farm_data['crop']}'")['group'].iloc[0]
        return crop_group
    
    def update_farm_dict(self):
        # Update the farm data dictionary with province after it's available
        self.farm_data['province'] = self.province
        self.farm_data['group'] = self.crop_group

    def validate_data(self):
    # Check if yield, area, and year are numeric
        if not isinstance(self.farm_data['yield'], (int, float)):
            raise TypeError("Yield must be a numeric value")
        if not isinstance(self.farm_data['area'], (int, float)):
            raise TypeError("Area must be a numeric value")
        if not isinstance(self.farm_data['start_year'], int):
            raise TypeError("Year must be an integer")
        if not isinstance(self.farm_data['end_year'], int):
            raise TypeError("Year must be an integer")
        
        # Check if yield and area are greater than 0
        if self.farm_data['yield'] <= 0:
            raise ValueError("Yield must be larger than 0")
        if self.farm_data['area'] <= 0:
            raise ValueError("Area must be larger than 0")
        
        # Check if year is within the valid range
        if not (1984 <= self.farm_data['start_year'] <= datetime.now().year):
            raise ValueError("Start year must be larger than 1984 and less than the current year")
        
        if not (1984 <= self.farm_data['end_year'] <= datetime.now().year):
            raise ValueError("End year must be larger than 1984 and less than the current year")

# Example usage
if __name__ == '__main__':
    input_file = 'data/test/litefarm_test.csv'
    farm_id = '0369f026-1f90-11ee-b788-0242ac150004'
    farm = FarmData(input_file=input_file, farm_id=farm_id, crop = 'Potato')
    print(farm.farm_data)

    # input_file2 = 'data/test/user_input_farm.json'
    # farm_id2 = 'farm123'
    # farm2 = FarmData(input_file=input_file2, farm_id=farm_id2)
    # print(farm2.farm_data)

