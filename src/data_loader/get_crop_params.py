import os
import pandas as pd
import numpy as np
import json
class CropParametersManager:
    def __init__(self, farm_data, climate_data):
        self.farm_data = farm_data
        self.crop = self.farm_data['crop']
        self.P = climate_data['P'][0]
        self.PE = climate_data['PE'][0]
        self.dir = os.path.dirname(__file__)
        self.crop_parameters_path = os.path.join(self.dir, '../../data/preprocessed/crop_parameters.csv')
        self.user_distributions_path = os.path.join(self.dir, '../../data/params_sampling_range/crop_params_dist.json')
        self.crop_parameters = self.get_crop_parameters()

    def get_crop_parameters(self):
        crop_params_df = pd.read_csv(self.crop_parameters_path)
        # Filter the dataframe for the given crop
        crop_params = crop_params_df[crop_params_df['crop'] == self.crop]

        # If only one row matches, return its parameters after cleaning
        if len(crop_params) == 1:
            selected_params = crop_params.iloc[0].to_dict()
            selected_params.pop('group', None)
            selected_params.pop('crop', None)
            selected_params.pop('condition', None)
            selected_params.pop('holos_crop_name', None)

            return {k: np.array([float(v)], dtype=np.float64) for k, v in selected_params.items()}

        selected_params = None  # This will store the selected row's dictionary

        # Process each row to find the best match according to the rules
        for _, row in crop_params.iterrows():
            condition = row['condition']
            
            # Priority for 'Canada'
            if condition == 'Canada':
                selected_params = row.to_dict()
                break  # Stop processing since 'Canada' has the highest priority

            # Handle 'irrigated' and 'rainfed' based on P and PE
            if self.P < self.PE and condition == 'Irrigated':
                selected_params = row.to_dict()  # Prefer 'irrigated' if P < PE

            elif self.P >= self.PE and condition == 'Rainfed':
                selected_params = row.to_dict()  # Prefer 'rainfed' otherwise

            # Handle numeric conditions with <, >, -
            elif '<' in condition:
                upper_bound = float(condition.replace('<', ''))
                if self.PE - self.P < upper_bound:
                    selected_params = row.to_dict()
                    
            elif '>' in condition:
                lower_bound = float(condition.replace('>', ''))
                if self.PE - self.P > lower_bound:
                    selected_params = row.to_dict()
                    
            elif '-' in condition:
                lower_bound, upper_bound = map(float, condition.split('-'))
                if lower_bound <= self.PE - self.P <= upper_bound:
                    selected_params = row.to_dict()

        if selected_params:
            # Clean up unnecessary data from the selected parameters
            selected_params.pop('group', None)
            selected_params.pop('crop', None)
            selected_params.pop('condition', None)
            selected_params.pop('holos_crop_name', None)

        return {k: np.array([float(v)], dtype=np.float64) for k, v in selected_params.items()}
    
    def load_user_distributions(self):
        with open(self.user_distributions_path, 'r') as file:
            return json.load(file)

    def sample_crop_parameters(self, sampling_mode='default', num_samples=10):
        sampled_parameters = {}
        if sampling_mode == 'default':
            for param, value in self.crop_parameters.items():
                value = value[0] 
                sampled_array = np.random.uniform(value * 0.75, value * 1.25, num_samples)
                sampled_parameters[param] = np.insert(sampled_array, 0, value)
        elif sampling_mode == 'user_define':
            user_distributions = self.load_user_distributions().get(self.crop, None)
        
            if user_distributions is None:
                raise ValueError(f"No user-defined distributions found for the crop '{self.crop}'.")
        
            for param, specs in user_distributions.items():
                distribution_type = specs[0]
                if distribution_type == 'uniform':
                    low, high = specs[1], specs[2]
                    sampled_array = np.random.uniform(low, high, num_samples)
                elif distribution_type == 'normal':
                    mean, sd = specs[1], specs[2]
                    sampled_array = np.random.normal(mean, sd, num_samples)
                elif distribution_type == 'lognormal':
                    mean, sigma = specs[1], specs[2]
                    sampled_array = np.random.lognormal(mean, sigma, num_samples)
                # Add more distribution types as needed in future
                value = self.crop_parameters[param][0]
                sampled_parameters[param] = np.insert(sampled_array, 0, value)
        else:
            raise ValueError("Invalid sampling mode specified.")
        
        return sampled_parameters   

if __name__ == '__main__':
    # Example farm and climate data setup for testing
    farm_data = {'crop': 'Oats'}

    climate_data = {'P': np.array([100]), 'PE': np.array([120])}

    # Initialize the CropParametersManager with the example data
    manager = CropParametersManager(farm_data, climate_data)

    # Fetch and print the crop parameters
    crop_parameters = manager.crop_parameters
    print("Crop Parameters:", crop_parameters)
    print(crop_parameters['moisture'].dtype)

    # Sample parameters with default settings
    default_samples = manager.sample_crop_parameters()
    print("Default Sampled Parameters:", default_samples)

    # Sample parameters with user-defined settings
    sampled_parameters = manager.sample_crop_parameters(sampling_mode='user_define')
    print("Sampled Parameters:", sampled_parameters)
