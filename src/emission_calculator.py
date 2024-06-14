import numpy as np

class EmissionCalculator:
    """
    A calculator for deriving nitrogen-based emissions and their equivalent CO2 impact from crop nitrogen residue and emission factor.

    Attributes:
        ef_data (dict): Validated input data containing emission factors.
        n_data (dict): Validated input data containing crop nitrogen residue.
        EF (float): Emission factor from validated input data.
        n_crop_residue (float): Crop nitrogen residue (CRN) value from validated input data.
    """

    def __init__(self, ef_data, n_data):
        """
        Initializes EmissionCalculator with the provided emission factor data and nitrogen data.

        Args:
            ef_data (dict): Input data containing emission factors.
            n_data (dict): Input data containing nitrogen values.

        Raises:
            ValueError: If essential keys are missing in the input data.
            TypeError: If the values under emission factor data or nitrogen data are not of type int or float.
        """
        self.validate_input(ef_data, n_data)
        self.ef_data = ef_data
        self.n_data = n_data
        self.EF = ef_data['EF']
        self.n_crop_residue = n_data['n_crop_residue']
        
    
    def validate_input(self, ef_data, n_data):
        """
        Validates the input data to ensure all required fields are present and correctly formatted.
        
        Args:
            ef_data (dict): The emission factor data to validate.
            n_data (dict): The nitrogen data to validate.

        Raises:
            ValueError: If required keys are missing from the emission factor data or nitrogen data.
            TypeError: If the values under emission factor data or nitrogen data are not of type int or float.
        """
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
        """
        Calculates the direct nitrogen emission from crop residue (n_crn_direct).
        Equation 2.6.5-2

        Returns:
            float: The direct nitrogen emission from crop residue.
        """
        self.n_crn_direct = self.n_crop_residue * self.EF

        return self.n_crn_direct
    
    def calculate_n_other_direct(self):
        """
        Sets the values for other sources of direct nitrogen emissions, currently set to 0. Can be modified to include other sources.
        """
        self.n_sn_direct = 0
        self.n_crnmin_direct = 0
        self.n_on_direct = 0
    
    def calculate_n_crop_direct(self):
        """
        Calculates the total direct nitrogen emission from all crop sources (n_crop_direct).
        Equation 2.6.9-1
        Returns:
            float: The total direct nitrogen emission from crops.
        """
        if not hasattr(self, 'n_sn_direct') or not hasattr(self, 'n_crnmin_direct') or not hasattr(self, 'n_on_direct'):
            self.calculate_n_other_direct()
        if not hasattr(self, 'n_crn_direct'):
            self.calculate_n_crn_direct()

        self.n_crop_direct = self.n_sn_direct + self.n_crnmin_direct + self.n_on_direct + self.n_crn_direct

        return self.n_crop_direct
    
    def convert_n_crop_direct_to_n2o(self):
        """
        Converts the total direct nitrogen emission from crops to N2O emissions.
        Using constant 44/28

        Returns:
            float: The N2O emissions derived from direct nitrogen emissions.
        """
        if not hasattr(self, 'n_crop_direct'):
            self.calculate_n_crop_direct()

        N_TO_NO2 = 44/28

        self.no2_crop_direct = self.n_crop_direct * N_TO_NO2

        return self.no2_crop_direct
    
    def calculate_n2o_crop_direct_to_co2e(self):
        """
        Calculates the CO2 equivalent of the N2O emissions from crop nitrogen emissions.
        Using constant 273, the same value used by Holos

        Returns:
            float: The CO2 equivalent of N2O emissions.
        """
        if not hasattr(self, 'no2_crop_direct'):
            self.convert_n_crop_direct_to_n2o()

        NO2_TO_CO2 = 273

        self.co2_crop_direct = self.no2_crop_direct * NO2_TO_CO2

        return self.co2_crop_direct
    
    def get_emission(self):
        """
        Retrieves the calculated emissions if available, or calculates them if not.

        Returns:
            dict: A dictionary containing all calculated emissions including nitrogen, N2O, and CO2 equivalent values.
        """
        if not hasattr(self, 'co2_crop_direct'):
            self.calculate_n2o_crop_direct_to_co2e()

        self.data_dict = {
            'n_crop_direct': self.n_crop_direct,
            'no2_crop_direct': self.no2_crop_direct,
            'co2_crop_direct': self.co2_crop_direct
        }

        return self.data_dict
    
if __name__ == "__main__":

    test_farm_n = {
        'n_crop_residue': 560.2468642105264
        }
    test_farm_ef = {
        'EF_CT_P': 0.001099631670775916,
        'EF_CT_PE': 0.019905484145844587,
        'EF_Topo': 0.0025232347031386142,
        'EF': 0.0032860731017619158
        }
    
    print('farm emission: ')
    emission_calculator = EmissionCalculator(test_farm_ef, test_farm_n)
    output = emission_calculator.get_emission()
    print(output)
    print("-"*50)