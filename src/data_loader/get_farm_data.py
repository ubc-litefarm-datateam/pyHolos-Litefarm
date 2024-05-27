import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from datetime import datetime

class FarmData:
    def __init__(self, input_file, farm_id):
        self.farm_id = farm_id
        self.dir = os.path.dirname(__file__)
        self.input_file_path = os.path.join(self.dir, '..', '..', input_file)
        self.farm_data = self.get_farm_data()
        self.farm_gdf = self.get_farm_gdf()
        self.province = self.get_province()

    def get_farm_data(self):
        df = pd.read_csv(self.input_file_path)
        df = df.query(f"farm_id == '{self.farm_id}'")
        if df.empty:
            raise ValueError(f"No farm data found for farm_id {self.farm_id}")

        df['area_in_m2'] = df['area_in_m2'].astype(float).map(lambda x: x * 0.0001)  # Convert and scale area
        df['yield_kg_per_m2'] = df['yield_kg_per_m2'].astype(float).map(lambda x: x * 10000)  # Convert and scale yield
        df['start_year'] = df['start_year'].astype(int)  # Ensure year is an integer
        df['end_year'] = df['end_year'].astype(int)

        farm = df.iloc[0].to_dict()

        farm['area'] = float(farm['area_in_m2'])
        farm['yield'] = float(farm['yield_kg_per_m2'])
        farm['start_year'] = int(farm['start_year'])
        farm['end_year'] = int(farm['end_year'])
        
        return {
            'area': farm['area'],
            'latitude': float(farm['lat']),
            'longitude': float(farm['lon']),
            'crop': farm['common_crop_name'],
            'yield': farm['yield'],
            'start_year': farm['start_year'],
            'end_year': farm['end_year']
        }

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
        province_shp_path = os.path.join(self.dir, '../../data/external/province_500m')
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
        
        # # Check if year is within the valid range
        # if not (1984 <= self.farm_data['year'] <= datetime.now().year):
        #     raise ValueError("Year must be larger than 1984 and less than the current year")

