import os
import json
import pandas as pd
import numpy as np

class CropGroupManager:
    def __init__(self, farm_data):
        self.farm_data = farm_data
        self.crop = self.farm_data['crop']
        self.dir = os.path.dirname(__file__)
        self.crop_to_group_map_path = os.path.join(
            self.dir, '../../data/preprocessed/crop_to_group.csv'
            )
        self.crop_group_params_path = os.path.join(
            self.dir, '../../data/preprocessed/crop_group_parameters.csv'
            )
        self.user_distributions_path = os.path.join(
            self.dir, '../../data/params_sampling_range/crop_group_params_dist.json')
        self.crop_group = self.get_crop_group()
        self.crop_group_params = self.get_crop_group_parameters()

    def get_crop_group(self):
        crop_to_group_map_df = pd.read_csv(self.crop_to_group_map_path)
        crop_group = crop_to_group_map_df.query(f"crop == '{self.crop}'")['group'].iloc[0]
        return crop_group

    def get_crop_group_parameters(self):
        crop_group_params_df = pd.read_csv(self.crop_group_params_path)
        crop_group_params = crop_group_params_df[crop_group_params_df['group'] == self.crop_group].iloc[0].to_dict()
        crop_group_params.pop('group', None)
        return {k: np.array([float(v)]) for k, v in crop_group_params.items()}
    
    def load_user_distributions(self):
        with open(self.user_distributions_path, 'r') as file:
            return json.load(file)
        
    def sample_crop_group_parameters(self, sampling_mode='default', num_samples=10):
        sampled_parameters = {}
        if sampling_mode == 'default':
            for param, value in self.crop_group_params.items():
                sampled_array = np.random.uniform(value * 0.75, value * 1.25, num_samples)
                sampled_parameters[param] = np.insert(sampled_array, 0, value)
        elif sampling_mode == 'user_define':
            user_distributions = self.load_user_distributions().get(self.crop_group, None)
            
            if user_distributions is None:
                raise ValueError(f"No user-defined distributions found for the crop group '{self.crop_group}'.")
            
            for param, specs in user_distributions.items():
                distribution_type = specs[0]
                # sampled_array = None
                if distribution_type == 'uniform':
                    low, high = specs[1], specs[2]
                    sampled_array = np.random.uniform(low, high, num_samples)
                elif distribution_type == 'normal':
                    mean, sd = specs[1], specs[2]
                    sampled_array = np.random.normal(mean, sd, num_samples)
                elif distribution_type == 'lognormal':
                    mean, sigma = specs[1], specs[2]
                    sampled_array = np.random.lognormal(mean, sigma, num_samples)
                
                # Ensure the parameter exists in crop_group_params before attempting to access it
                if param in self.crop_group_params:
                    value = self.crop_group_params[param]
                    sampled_parameters[param] = np.insert(sampled_array, 0, value)
                else:
                    raise KeyError(f"Parameter '{param}' not found in crop group parameters.")
        else:
            raise ValueError("Invalid sampling mode specified or undefined user distributions.")

        return sampled_parameters

# Example usage
if __name__ == '__main__':
    # Example farm_data containing 'crop' information
    farm_data = {'crop': 'Wheat'}
    manager = CropGroupManager(farm_data)
    print("Crop Group Parameters:", manager.crop_group_params)
    
    default_samples = manager.sample_crop_group_parameters()
    print("Default Sampled Parameters:", default_samples)

    try:
        user_defined_samples = manager.sample_crop_group_parameters(sampling_mode='user_define')
        print("User-defined Sampled Parameters:", user_defined_samples)
    except ValueError as e:
        print(e)