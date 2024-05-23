import numpy as np

class EmissionCalculator:
    def __init__(self, ef_data, n_data):
        ## validate input data
        self.validate_input(ef_data, n_data)
        ## initialize instance variables with validated data
        self.ef_data = ef_data
        self.n_data = n_data
        self.EF = ef_data['EF']
        self.n_crop_residue = n_data['n_crop_residue']
        
    
    def validate_input(self, ef_data, n_data):
        ## data should include all required fields and should be numbers
        required_ef_key = ['EF']
        for key in required_ef_key:
            if key not in ef_data:
                raise ValueError(f"Missing required key: {key}")
            if not isinstance(ef_data[key], (int, float, np.number)):
                raise TypeError(f"Value for {key} must be a number (int or float)")
            
        required_n_keys = ['n_crop_residue']
        for key in required_n_keys:
            if key not in n_data:
                raise ValueError(f"Missing required key: {key}")
            if not isinstance(n_data[key], (int, float, np.number)):
                raise TypeError(f"Value for {key} must be a number (int or float)")     
            
    def calculate_n_crn_direct(self):
        ## calculate n_crn_direct
        ## equation 2.6.5-2
        self.n_crn_direct = self.n_crop_residue * self.EF

        return self.n_crn_direct
    
    def calculate_n_other_direct(self):
        ## set values for other sources of n_direct
        ## currently set to 0, cen be modified to include other sources
        self.n_sn_direct = 0
        self.n_crnmin_direct = 0
        self.n_on_direct = 0
    
    def calculate_n_crop_direct(self):
        ## calculate n_crop_direct
        ## equation 2.6.9-1
        if not hasattr(self, 'n_sn_direct') or not hasattr(self, 'n_crnmin_direct') or not hasattr(self, 'n_on_direct'):
            self.calculate_n_other_direct()
        if not hasattr(self, 'n_crn_direct'):
            self.calculate_n_crn_direct()

        self.n_crop_direct = self.n_sn_direct + self.n_crnmin_direct + self.n_on_direct + self.n_crn_direct

        return self.n_crop_direct
    
    def convert_n_crop_direct_to_n2o(self):
        ## calculate n02_crop_direct using n_crop_direct
        ## using constant 44/28
        if not hasattr(self, 'n_crop_direct'):
            self.calculate_n_crop_direct()

        N_TO_NO2 = 44/28

        self.no2_crop_direct = self.n_crop_direct * N_TO_NO2

        return self.no2_crop_direct
    
    def calculate_n2o_crop_direct_to_co2e(self):
        ## calculate co2 equavilent for n2o_crop_direct
        ## using constant 273, the same value used by Holos
        if not hasattr(self, 'no2_crop_direct'):
            self.convert_n_crop_direct_to_n2o()

        NO2_TO_CO2 = 273

        self.co2_crop_direct = self.no2_crop_direct * NO2_TO_CO2

        return self.co2_crop_direct
    
    def get_emission(self):
        if not hasattr(self, 'co2_crop_direct'):
            self.calculate_n2o_crop_direct_to_co2e()

        self.data_dict = {
            'n_crop_direct': self.n_crop_direct,
            'no2_crop_direct': self.no2_crop_direct,
            'co2_crop_direct': self.co2_crop_direct
        }

        return self.data_dict