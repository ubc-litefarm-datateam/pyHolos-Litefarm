import os
import pandas as pd

class CropGroupManager:
    def __init__(self, farm_data, climate_data):
        self.farm_data = farm_data  
        self.dir = os.path.dirname(__file__)
        self.crop_group = self.get_crop_group()
        self.crop_group_params = self.get_crop_group_parameters()

    def get_crop_group(self):
        crop = self.farm_data.farm_data['crop'].lower()
        crop_to_group_map_path = os.path.join(self.dir, 
                                              '../../data/preprocessed/crop_to_group.csv')
        crop_to_group_map_df = pd.read_csv(crop_to_group_map_path)
        crop_group = crop_to_group_map_df.query(f"crop == '{crop}'")['group'].iloc[0]
        return crop_group

    def get_crop_group_parameters(self):
        crop_group_params_path = os.path.join(self.dir, 
                                              '../../data/preprocessed/crop_group_parameters.csv')
        crop_group_params_df = pd.read_csv(crop_group_params_path)
        crop_group_params = crop_group_params_df[crop_group_params_df['group'] == self.crop_group].iloc[0].to_dict()
        return crop_group_params
