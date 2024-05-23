import math
import numpy as np

class EmissionFactorCalculator:

    def __init__(self ,farm_data):
        ## validate input data
        self.validate_input(farm_data)
        ## initialize instance variables with validated data
        self.data = farm_data
        self.P = farm_data['climate_data']['P']
        self.PE = farm_data['climate_data']['PE']
        self.FR_Topo = farm_data['climate_data']['FR_Topo']
        self.RF_TX = farm_data['modifiers']['RF_TX']
        self.RF_NS = farm_data['modifiers']['RF_NS']
        self.RF_till = farm_data['modifiers']['RF_Till']
        self.RF_CS = farm_data['modifiers']['RF_CS']
        self.RF_AM = farm_data['modifiers']['RF_AM']

    def validate_input(self, farm_data):
        ## data should include all required fields and should be numbers
        required_climate_keys = ['P', 'PE', 'FR_Topo']
        
        for key in required_climate_keys:
            if key not in farm_data['climate_data']:
                raise ValueError(f"Missing required climate data key: {key}")
                print(key)
            if not isinstance(farm_data['climate_data'][key], (int, float, np.number)):
                raise TypeError(f"Value for climate_data[{key}] must be a number (int or float)")
    
        required_modifiers_keys = ['RF_TX', 'RF_NS', 'RF_Till', 'RF_CS', 'RF_AM']
        for key in required_modifiers_keys:
            if key not in farm_data['modifiers']:
                raise ValueError(f"Missing required modifiers key: {key}")
            if not isinstance(farm_data['modifiers'][key], (int, float, np.number)):
                raise TypeError(f"Value for modifiers[{key}] must be a number (int or float)")    

    def calculate_ef_ct(self):
        ## calculate EF_CT_P and EF_CT_PE based on P and PE 
        ## equation 2.5.1-1 and 2.5.1-2
        self.EF_CT_P = math.exp(0.00558 * self.P - 7.7)
        self.EF_CT_PE = math.exp(0.00558 * self.PE - 7.7)

        return self.EF_CT_P, self.EF_CT_PE
    
    def calculate_ef_topo(self):
        ## calculate EF_Topo
        ## equation 2.5.2-1, 2.5.2-2, and 2.5.2-3
        ## ensure EF_CT_P and EF_CT_PE are calculated
        if not hasattr(self, 'EF_CT_P') or not hasattr(self, 'EF_CT_PE'):
            self.calculate_ef_ct()

        intermediate_factor = self.P/self.PE

        if intermediate_factor > 1:
            self.EF_Topo = self.EF_CT_P
        elif self.P == self.PE:
            self.EF_Topo = self.EF_CT_PE
        else:
            self.EF_Topo = ((self.EF_CT_PE * self.FR_Topo/100) + (self.EF_CT_P * (1 - self.FR_Topo/100)))

        return self.EF_Topo
    
    def calculate_emission_factor(self):
        ## calculate emission factor
        ## equation 2.5.3-2 and 2.5.4-1
        ## ensure EF_CT_P and EF_CT_PE are calculated
        if not hasattr(self, 'EF_Topo'):
            self.calculate_ef_topo()
        
        EF_base = (self.EF_Topo*self.RF_TX) * (1/0.645)

        self.EF = EF_base * self.RF_NS * self.RF_till * self.RF_CS * self.RF_AM

        return self.EF
    
    def get_ef(self):
        if not hasattr(self, 'EF'):
            self.calculate_emission_factor()

        self.data_dict = {'EF_CT_P': self.EF_CT_P,
                          'EF_CT_PE': self.EF_CT_PE,
                          'EF_Topo': self.EF_Topo,
                          'EF': self.EF}
        
        return self.data_dict