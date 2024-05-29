import numpy as np
import copy
import warnings
from crop_residue_calculator import CropResidueCalculator

class SensitivityCrnCalculator:
    """
    Handles array inputs for the CropResidueCalculator, allowing for analysis with changes
    in multiple nested parameters. Calculates variations for every subkey in the data automatically.
    """
    def __init__(self, data, operation_mode):
        """
        Initialize with the data containing nested dictionaries and numpy arrays.
        """
        self.data = data
        self.mode = operation_mode
        self.validate_mode_data_compatibility()
        self.baseline_data = self.get_baseline_data()
        self.calculator = CropResidueCalculator(self.baseline_data)
    
    def validate_mode_data_compatibility(self):
        """
        Checks that the length of arrays in data matches the expected length for the selected mode.
        Raises an error or warning if there is a mismatch.
        """
        all_single_value = True
        for params in self.data.values():
            for values in params.values():
                if isinstance(values, np.ndarray) and len(values) > 1:
                    all_single_value = False
                    break

        if self.mode == 'scientific' and all_single_value:
            warnings.warn("All parameters have only one value. Switching to farmer mode.", UserWarning)
            self.mode = 'farmer'  # Change mode to farmer

        for params in self.data.values():
            for values in params.values():
                if isinstance(values, np.ndarray):
                    if self.mode == 'farmer' and len(values) != 1:
                        raise ValueError("Length of the parameters should be 1 for farmer mode.")
                    elif self.mode == 'scientific' and len(values) < 1:
                        raise ValueError("Length of the parameters should be longer than 1 for scientific mode.")

    def get_baseline_data(self):
        """
        Creates baseline data by taking the first element of each numpy array in nested dictionaries.

        Example:
        From:
        {
            'farm_data': {
                'area': np.array([100, 150, 200]),
                'yield': np.array([5000, 6000, 7000])
            },
            'crop_parameters': {
                'moisture': np.array([14, 15, 16]),
                'carbon_concentration': np.array([0.4, 0.5, 0.6])
            }
        }
        To:
        {
            'farm_data': {
                'area': 100,
                'yield': 5000
            },
            'crop_parameters': {
                'moisture': 14,
                'carbon_concentration': 0.4
            }
        }
        """
        baseline = {}
        for data_type, params in self.data.items():
            baseline[data_type] = {}
            for parameter, value in params.items():
                if isinstance(value, np.ndarray):
                    baseline[data_type][parameter] = value[0]
                else:
                    baseline[data_type][parameter] = value
        return baseline

    def crop_analysis(self):
            """
            Determines calculation mode and executes accordingly.
            """
            if self.mode == 'farmer':
                return self.farmer_mode()
            elif self.mode == 'scientific':
                return self.scientific_mode()

    def farmer_mode(self):
        """
        Handles the 'farmer' mode where only a single set of calculations based on the baseline data is needed.
        """
        results = {}
        calculator = CropResidueCalculator(self.baseline_data)
        results['C_p'] = [calculator.c_p()]
        results['above_ground_carbon_input'] = [calculator.above_ground_carbon_input()]
        results['below_ground_carbon_input'] = [calculator.below_ground_carbon_input()]
        results['above_ground_residue_n'] = [calculator.above_ground_residue_n()]
        results['below_ground_residue_n'] = [calculator.below_ground_residue_n()]
        results['n_crop_residue'] = [calculator.n_crop_residue()]
        return results

    def scientific_mode(self):
        """
        Handles the 'scientific' mode where variations for parameters with more than one value are calculated.
        """
        results = {}
        for data_type, params in self.data.items():
            for parameter, values in params.items():
                if isinstance(values, np.ndarray):
                    results[parameter] = {
                        'C_p': [],
                        'above_ground_carbon_input': [],
                        'below_ground_carbon_input': [],
                        'above_ground_residue_n': [],
                        'below_ground_residue_n': [],
                        'n_crop_residue': []
                    }

                    for value in values:
                        temp_data = copy.deepcopy(self.baseline_data)
                        temp_data[data_type][parameter] = value
                        calculator = CropResidueCalculator(temp_data)
                        results[parameter]['C_p'].append(calculator.c_p())
                        results[parameter]['above_ground_carbon_input'].append(calculator.above_ground_carbon_input())
                        results[parameter]['below_ground_carbon_input'].append(calculator.below_ground_carbon_input())
                        results[parameter]['above_ground_residue_n'].append(calculator.above_ground_residue_n())
                        results[parameter]['below_ground_residue_n'].append(calculator.below_ground_residue_n())
                        results[parameter]['n_crop_residue'].append(calculator.n_crop_residue())
        return results

if __name__ == "__main__":

    data_sci = {
        'farm_data': {
            'area': np.array([100]),  
            'yield': np.array([5000]), 
        },
        'crop_group_params': {
            'group': np.array(['annual', 'perennial', 'cover']),  
            'S_p': np.array([90, 85, 80]),
            'S_s': np.array([70, 75, 80]),
            'S_r': np.array([60, 65, 70]),
            'carbon_concentration': np.array([0.4, 0.5, 0.6]), 
        },
        'crop_parameters': {
            'moisture': np.array([14, 15, 16]),
            'R_p': np.array([0.1, 0.2, 0.3]),
            'R_s': np.array([0.1, 0.15, 0.2]),
            'R_r': np.array([0.05, 0.1, 0.15]),
            'R_e': np.array([0.01, 0.02, 0.03]),
            'N_p': np.array([1, 2, 3]),
            'N_s': np.array([1.5, 2.5, 3.5]),
            'N_r': np.array([1, 1.5, 2]),
            'N_e': np.array([0.5, 0.75, 1])
        }
    }

    data_farm = {
    'farm_data': {
        'area': np.array([100]),  
        'yield': np.array([5000]),  # Yield in kg/ha
    },
    'crop_group_params': {
        'group': np.array(['annual']), 
        'S_p': np.array([90]),
        'S_s': np.array([70]),
        'S_r': np.array([60]),
        'carbon_concentration': np.array([0.4]), 
    },
    'crop_parameters': {
        'moisture': np.array([14]),
        'R_p': np.array([0.1]),
        'R_s': np.array([0.1]),
        'R_r': np.array([0.05]),
        'R_e': np.array([0.01]),
        'N_p': np.array([1]),
        'N_s': np.array([1.5]),
        'N_r': np.array([1]),
        'N_e': np.array([0.5])
    }
}

    print('If operation mode is farmer and lengths of the parameters are 1:')
    farmer_calc = SensitivityCrnCalculator(data_farm, 'farmer')
    print(farmer_calc.crop_analysis())
    print("-"*50)
    print("\n"*2)
    print('If operation mode is scientific but the lengths of the parameters are 1:')
    sci_calc = SensitivityCrnCalculator(data_farm, 'scientific')
    print(sci_calc.crop_analysis())
    print("-"*50)
    print("\n"*2)
    print('If operation mode is scientific and the lengths of the parameters are more than 1:')
    sci_calc = SensitivityCrnCalculator(data_sci, 'scientific')
    print(sci_calc.crop_analysis())
    