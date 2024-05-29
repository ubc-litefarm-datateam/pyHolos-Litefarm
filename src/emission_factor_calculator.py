import math
import numpy as np

class EmissionFactorCalculator:
    """
    A calculator for emission factors based on climatic and modifiers for selected farm.
    
    Attributes
    ----------
    data (dict): The validated input data containing necessary climate and modifier parameters.
    P (float): Precipitation data from climate data.
    PE (float): Potential evapotranspiration from climate data.
    FR_Topo (float): Fractional contribution from topographical data.
    RF_TX (float): Regional factor for temperature extremes.
    RF_NS (float): Regional factor for nitrogen stress.
    RF_till (float): Reduction factor due to tillage practices.
    RF_CS (float): Reduction factor for crop sequence.
    RF_AM (float): Adjustment factor for management practices.
    """

    def __init__(self ,farm_data):
        """
        Initializes EmissionFactorCalculator with the provided farm data.
        
        Args:
            farm_data (dict): Farm data containing climate data and modifiers.
        
        Raises:
            ValueError: If essential keys are missing in the input data.
            TypeError: If the values under climate data or modifiers are not of type int or float.
        """
        self.validate_input(farm_data)
        self.data = farm_data
        self.P = farm_data['climate_data']['P']
        self.PE = farm_data['climate_data']['PE']
        self.FR_Topo = farm_data['climate_data']['FR_Topo']
        self.RF_TX = farm_data['climate_data']['soil_texture']
        self.RF_NS = farm_data['modifiers']['RF_NS']
        self.RF_till = farm_data['modifiers']['RF_Till']
        self.RF_CS = farm_data['modifiers']['RF_CS']
        self.RF_AM = farm_data['modifiers']['RF_AM']

    def validate_input(self, farm_data):
        """
        Validates input data to ensure all required fields are present and correctly formatted.
        
        Args:
            farm_data (dict): The input data to validate.
        
        Raises:
            ValueError: If required keys are missing from the climate data or modifiers.
            TypeError: If the values under climate data or modifiers are not of type int or float.
        """
        required_climate_keys = ['P', 'PE', 'FR_Topo', 'soil_texture']
        
        for key in required_climate_keys:
            if key not in farm_data['climate_data']:
                raise ValueError(f"Missing required climate data key: {key}")
                print(key)
            if not isinstance(farm_data['climate_data'][key], (int, float, np.number)):
                raise TypeError(f"Value for climate_data[{key}] must be a number (int or float)")
    
        required_modifiers_keys = ['RF_NS', 'RF_Till', 'RF_CS', 'RF_AM']
        for key in required_modifiers_keys:
            if key not in farm_data['modifiers']:
                raise ValueError(f"Missing required modifiers key: {key}")
            if not isinstance(farm_data['modifiers'][key], (int, float, np.number)):
                raise TypeError(f"Value for modifiers[{key}] must be a number (int or float)")    

    def calculate_ef_ct(self):
        """
        Calculates EF_CT_P and EF_CT_PE based on precipitation (P) and evapotranspiration (PE).
        Equation 2.5.1-1 and 2.5.1-2

        Returns:
            tuple: A tuple containing EF_CT_P and EF_CT_PE values.
        """
        self.EF_CT_P = math.exp(0.00558 * self.P - 7.7)
        self.EF_CT_PE = math.exp(0.00558 * self.PE - 7.7)

        return self.EF_CT_P, self.EF_CT_PE
    
    def calculate_ef_topo(self):
        """
        Calculates topographical emission factor (EF_Topo) considering both climatic and topographical modifiers.
        Equation 2.5.2-1, 2.5.2-2, and 2.5.2-3

        Returns:
            float: The calculated EF_Topo.
        """
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
        """
        Calculates the overall emission factor (EF) based on climatic and modifiers.
        Equation 2.5.3-2 and 2.5.4-1

        Returns:
            float: The calculated EF.
        """
        if not hasattr(self, 'EF_Topo'):
            self.calculate_ef_topo()
        
        EF_base = (self.EF_Topo*self.RF_TX) * (1/0.645)

        self.EF = EF_base * self.RF_NS * self.RF_till * self.RF_CS * self.RF_AM

        return self.EF
    
    def get_ef(self):
        """
        Retrieves calculated emission factors if available, or calculates them if not.
        
        Returns:
            dict: A dictionary containing all calculated emission factors.
        """
        if not hasattr(self, 'EF'):
            self.calculate_emission_factor()

        self.data_dict = {'EF_CT_P': self.EF_CT_P,
                          'EF_CT_PE': self.EF_CT_PE,
                          'EF_Topo': self.EF_Topo,
                          'EF': self.EF}
        
        return self.data_dict