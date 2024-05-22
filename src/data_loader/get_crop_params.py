import os
import pandas as pd

class CropParametersManager:
    def __init__(self, farm_data):
        self.farm_data = farm_data  
        self.dir = os.path.dirname(__file__)
        self.crop_parameters = self.get_crop_parameters() 

    def get_crop_parameters(self):
        crop = self.farm_data.farm_data['crop']
        crop_params_path = os.path.join(self.dir, '../../data/preprocessed/crop_parameters.csv')
        crop_params_df = pd.read_csv(crop_params_path)

        # Assuming 'crop' column is used to find the specific crop parameters
        crop_params = crop_params_df[crop_params_df['crop'] == crop].iloc[0].to_dict()
        crop_params.pop('group', None)  # Remove 'group' as it's not needed
        crop_params.pop('holos_crop_name', None)  # Remove 'holos_crop_name' as it's not needed

        return crop_params
