import os
import pandas as pd
import geopandas as gpd

class ClimateDataExtractor:
    def __init__(self, farm_data):
        self.farm_data = farm_data
        self.dir = os.path.dirname(__file__)
        self.climate_dict = None

    def load_climate_data(self):
        climate_path = os.path.join(self.dir, '../../data/raw/Holos/ecodistrict_to_ecozone_mapping.csv')
        return pd.read_csv(climate_path)
    
    def load_slc_polygons(self):
        slc_polygons_path = os.path.join(self.dir, '../../data/external/slc')
        slc_polygons = gpd.read_file(slc_polygons_path)
        slc_polygons.set_crs('EPSG:4269', inplace=True)
        return slc_polygons.to_crs('EPSG:4326')
        
    def extract_climate_data(self):
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
        return self.climate_dict

