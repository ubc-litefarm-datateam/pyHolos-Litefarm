import numpy as np
from emission_factor_calculator import EmissionFactorCalculator
class SensitivityEmissionFactor:
    def __init__(self, farm_data, operation_mode = 'farmer'):
        self.farm_data = farm_data
        self.variables = list(farm_data['climate_data'].keys()) + list(farm_data['modifiers'].keys())
        self.mode = operation_mode
        self.results = {}
        self.output = {}

    def perform_analysis(self):
        # Iterating over all variables
        for variable in self.variables:
            # Initialize dictionary for each variable to store lists of results
            self.results[variable] = {}
            # Extract array values for the current variable
            values_array = self.farm_data['climate_data'].get(variable, []) + self.farm_data['modifiers'].get(variable, [])
            
            # Initialize results storage for this variable
            init_dict = {}
            for index in range(len(values_array)):
                modified_data = self.prepare_data_for_efc(variable, values_array[index])
                efc = EmissionFactorCalculator(modified_data)
                ef_results = efc.get_ef()
                
                # Initialize dictionary to collect results by ef type
                if index == 0:  # Setup the dictionary with keys and empty lists
                    for key in ef_results.keys():
                        init_dict[key] = []
                
                # Append results to the corresponding key
                for key, value in ef_results.items():
                    init_dict[key].append(value)
            
            # Store aggregated results
            for key, value_list in init_dict.items():
                self.results[variable][key] = np.array(value_list)
        
        return self.results
    
    def get_result(self):
        output_temp = self.perform_analysis()
        if self.mode == 'farmer':
            self.output = output_temp['P']
        elif self.mode == 'scientific':
            self.output = output_temp
            
        return self.output

    def prepare_data_for_efc(self, selected_variable, value):
        data = {'climate_data': {}, 'modifiers': {}}
        # Initialize all variables with their default values
        for var in self.variables:
            if var in self.farm_data['climate_data']:
                data['climate_data'][var] = self.farm_data['climate_data'][var][0]
            if var in self.farm_data['modifiers']:
                data['modifiers'][var] = self.farm_data['modifiers'][var][0]
        
        # Replace the value of the selected variable with the current value from its array
        if selected_variable in data['climate_data']:
            data['climate_data'][selected_variable] = value
        elif selected_variable in data['modifiers']:
            data['modifiers'][selected_variable] = value
        
        return data