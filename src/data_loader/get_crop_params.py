import os
import pandas as pd

# class CropParametersManager:
#     def __init__(self, farm_data):
#         self.farm_data = farm_data  
#         self.dir = os.path.dirname(__file__)
#         self.crop_parameters = self.get_crop_parameters() 

#     def get_crop_parameters(self):
#         crop = self.farm_data.farm_data['crop']
#         crop_params_path = os.path.join(self.dir, '../../data/preprocessed/crop_parameters.csv')
#         crop_params_df = pd.read_csv(crop_params_path)

#         # Assuming 'crop' column is used to find the specific crop parameters
#         crop_params = crop_params_df[crop_params_df['crop'] == crop].iloc[0].to_dict()
#         crop_params.pop('group', None)  # Remove 'group' as it's not needed
#         crop_params.pop('holos_crop_name', None)  # Remove 'holos_crop_name' as it's not needed

#         return crop_params

class CropParametersManager:
    def __init__(self, farm_data, climate_data):
        self.farm_data = farm_data
        self.P = climate_data['P']
        self.PE = climate_data['PE']
        self.dir = os.path.dirname(__file__)
        self.crop_parameters = self.get_crop_parameters()

    def get_crop_parameters(self):
        crop = self.farm_data.farm_data['crop']
        crop_params_path = os.path.join(self.dir, '../../data/preprocessed/crop_parameters.csv')
        crop_params_df = pd.read_csv(crop_params_path)

        # Filter the dataframe for the given crop
        crop_params = crop_params_df[crop_params_df['crop'] == crop]

        # If only one row matches, return its parameters after cleaning
        if len(crop_params) == 1:
            selected_params = crop_params.iloc[0].to_dict()
            selected_params.pop('group', None)
            selected_params.pop('crop', None)
            selected_params.pop('condition', None)
            selected_params.pop('holos_crop_name', None)
            return selected_params

        selected_params = None  # This will store the selected row's dictionary

        # Process each row to find the best match according to the rules
        for _, row in crop_params.iterrows():
            condition = row['condition']
            
            # Priority for 'Canada'
            if condition == 'Canada':
                selected_params = row.to_dict()
                break  # Stop processing since 'Canada' has the highest priority

            # Handle 'irrigated' and 'rainfed' based on P and PE
            if self.P < self.PE and condition == 'irrigated':
                selected_params = row.to_dict()  # Prefer 'irrigated' if P < PE

            elif self.P >= self.PE and condition == 'rainfed':
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

        return selected_params  # Return the accumulated result or None if no match found

