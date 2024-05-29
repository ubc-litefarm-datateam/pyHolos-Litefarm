from emission_calculator import EmissionCalculator
import numpy as np
class SensitivityEmission:
    def __init__(self, ef_data, n_data, operation_mode = 'farmer'):
        self.ef_data = ef_data
        self.n_data = n_data
        self.variables = list(ef_data.keys()) + list(n_data.keys())
        self.mode = operation_mode
        self.results = {}
        self.output = {}

    def perform_analysis(self):
        # Iterating over all variables
        for variable in self.variables:
            # Initialize dictionary for each variable to store lists of results
            self.results[variable] = {}
            # Extract array values for the current variable
            if variable in self.ef_data.keys():
                values_array = self.ef_data.get(variable).get('EF')
            elif variable in self.n_data.keys():
                values_array = self.n_data.get(variable).get('n_crop_residue')
            
            # Initialize results storage for this variable
            init_dict = {}
            for index in range(len(values_array)):
                modified_ef = self.prepare_ef_input_for_ec(variable, values_array[index])
                modified_n = self.prepare_n_input_for_ec(variable, values_array[index])
                ec = EmissionCalculator(modified_ef, modified_n)
                emission_results = ec.get_emission()
                
                # Initialize dictionary to collect results
                if index == 0:  # Setup the dictionary with keys and empty lists
                    for key in emission_results.keys():
                        init_dict[key] = []
                
                # Append results to the corresponding key
                for key, value in emission_results.items():
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
    
    def prepare_ef_input_for_ec(self, selected_variable, value):

        ef_input = {'EF': self.ef_data.get('P').get('EF')[0]}
        if selected_variable in self.ef_data:
            ef_input['EF'] = value
        return ef_input


    def prepare_n_input_for_ec(self, selected_variable, value):
        n_input = {'n_crop_residue': self.n_data.get('moisture').get('n_crop_residue')[0]}
        
        if selected_variable in self.n_data:
            n_input['n_crop_residue'] = value
        return n_input  
    