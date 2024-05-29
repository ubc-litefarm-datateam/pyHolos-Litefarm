import os
import json
import numpy as np
import pandas as pd
# import geopandas as gpd

class Modifiers:
    def __init__(self, farm_data):
        self.farm_data = farm_data
        self.dir = os.path.dirname(__file__)
        self.modifiers = self.get_modifiers()
        self.user_distributions_path = os.path.join(self.dir, '../../data/params_sampling_range/rf_params_dist.json')


    def get_modifiers(self, rf_am='default', rf_cs='Annual', rf_ns='RF_NS_CRN', tillage='unknown'):
        region = self.get_region()
        modifiers = {}
        # Define the list of modifiers and the relevant files
        modifier_files = {
            'RF_AM': 'modifier_rf_am.csv',
            'RF_CS': 'modifier_rf_cs.csv',
            'RF_NS': 'modifier_rf_ns.csv',
            'RF_Till': 'modifier_rf_till.csv'
        }

        # Iterate over the modifier files, loading and querying as needed
        for key, filename in modifier_files.items():
            path = os.path.join(self.dir, f'../../data/preprocessed/{filename}')
            df = pd.read_csv(path)
            
            if key == 'RF_AM':
                value = df.query(f"method == '{rf_am}'")['value'].iloc[0]
            elif key == 'RF_CS':
                value = df.query(f"group == '{rf_cs}'")['value'].iloc[0]
            elif key == 'RF_NS':
                value = df.query(f"N_source == '{rf_ns}'")['value'].iloc[0]
            elif key == 'RF_Till':
                value = df.query(f"region == '{region}' & tillage == '{tillage}'")['value'].iloc[0]

            modifiers[key] = value

        return {k: np.array([v]) for k, v in modifiers.items()}

    def get_region(self):
        province = self.farm_data['province']
        western_canada = ['Alberta', 'British Columbia', 
                          'Manitoba', 'Saskatchewan', 
                          'Northwest Territories', 'Nunavut']
        
        return 'western_canada' if province in western_canada else 'eastern_canada'
        
    def load_user_distributions(self):
        with open(self.user_distributions_path, 'r') as file:
            return json.load(file)

    def sample_modifiers(self, sampling_mode='default', num_samples=10):
        sampled_parameters = {}

        # Load user distributions only if the sampling mode is 'user_define'
        if sampling_mode == 'user_define':
            region = self.get_region()
            user_distributions = self.load_user_distributions()
            if user_distributions is None:
                raise ValueError("No user-defined RF distributions found.")
        else:
            user_distributions = None

        for param, value in self.modifiers.items():
            if sampling_mode == 'default':
                sampled_array = np.random.uniform(value * 0.75, value * 1.25, num_samples)
                sampled_parameters[param] = np.insert(sampled_array, 0, value)
            elif sampling_mode == 'user_define':
                specs = user_distributions[param]
                if specs:
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
                    sampled_parameters[param] = np.insert(sampled_array, 0, value)
                else:
                    raise KeyError(f"Parameter '{param}' not found in RF parameters.")
            else:
                raise ValueError("Invalid sampling mode specified or undefined user distributions.")

        return sampled_parameters

# Example usage
if __name__ == '__main__':
    farm_data = {'Province': 'Alberta'}
    mod = Modifiers(farm_data)
    print("Calculated Modifiers:", mod.modifiers)
    
    default_samples = mod.sample_modifiers()
    print("Default Sampled Modifiers:", default_samples)

    try:
        user_defined_samples = mod.sample_modifiers(sampling_mode='user_define')
        print("User-defined Sampled Modifiers:", user_defined_samples)
    except ValueError as e:
        print(e)