import sys
import os
import numpy as np
import copy
import warnings

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.calculator.crop_residue_calculator import CropResidueCalculator


class CropResidueAggregator:
    """
    A class to handle dictionary of array inputs for the CropResidueCalculator,
    allowing for analysis with changes in multiple nested parameters.
    Calculates variations for every parameter in the data automatically.

    Parameters
    ----------
    data : dict
        A dictionary containing nested dictionaries and numpy arrays with crop data.
    operation_mode : str
        The mode of operation, either 'farmer' or 'scientific'.

    Attributes
    ----------
    data : dict
        The input data containing nested dictionaries and numpy arrays.
    mode : str
        The mode of operation.
    target_data_group : list of str
        The list of target data groups to be processed.
    baseline_data : dict
        The baseline data created by taking the first element of each numpy array
        in nested dictionaries.
    calculator : CropResidueCalculator
        An instance of CropResidueCalculator initialized with baseline data.

    Methods
    -------
    validate_mode_data_compatibility()
        Checks that the length of arrays in data matches the expected length for
        the selected mode.Raises an error or warning if there is a mismatch.
    get_baseline_data()
        Creates baseline data by taking the first element of each numpy array in
        nested dictionaries.
    crop_analysis()
        Determines calculation mode and executes accordingly.
    farmer_mode()
        Handles the 'farmer' mode where only a single set of calculations.
    scientific_mode()
        Handles the 'scientific' mode where variations for parameters with more
        than one value are calculated.

    Examples
    --------
    >>> data_farm = {
    >>>     'farm_data': {
    >>>         'area': np.array([0.1409]),
    >>>         'latitude': np.array([46.4761852]),
    >>>         'longitude': np.array([-71.5189528]),
    >>>         'crop': np.array(['Soybean'], dtype='<U7'),
    >>>         'yield': np.array([2700.]),
    >>>         'start_year': np.array([2021]),
    >>>         'end_year': np.array([2021]),
    >>>         'province': np.array(['Quebec'], dtype='<U6'),
    >>>         'group': np.array(['annual'])
    >>>     },
    >>>     'crop_group_params': {
    >>>         'carbon_concentration': np.array([0.45]),
    >>>         'S_s': np.array([100.]),
    >>>         'S_r': np.array([100.]),
    >>>         'S_p': np.array([2.])
    >>>     },
    >>>     'crop_parameters': {
    >>>         'moisture': np.array([14.]),
    >>>         'R_p': np.array([0.304]),
    >>>         'R_s': np.array([0.455]),
    >>>         'R_r': np.array([0.146]),
    >>>         'R_e': np.array([0.095]),
    >>>         'N_p': np.array([67.]),
    >>>         'N_s': np.array([6.]),
    >>>         'N_r': np.array([10.]),
    >>>         'N_e': np.array([10.])
    >>>     },
    >>>     'climate_data': {
    >>>         'P': np.array([652.]),
    >>>         'PE': np.array([556.]),
    >>>         'FR_Topo': np.array([11.71]),
    >>>         'locations': np.array([[-71.5189528,  46.4761852]]),
    >>>         'soil_texture': np.array([0.49])
    >>>     },
    >>>     'modifiers': {
    >>>         'RF_AM': np.array([1.]),
    >>>         'RF_CS': np.array([1.]),
    >>>         'RF_NS': np.array([0.84]),
    >>>         'RF_Till': np.array([1.])
    >>>     }
    >>> }
    >>> sci_calc = CropResidueAggregator(data_farm, 'farmer')
    >>> sci_calc.crop_analysis()
    """

    def __init__(self, data, operation_mode):
        """
        Initialize with the data containing nested dictionaries and numpy arrays.
        """
        self.data = data
        self.mode = operation_mode
        self.target_data_group = ["crop_group_params", "crop_parameters"]
        self.validate_mode_data_compatibility()
        self.baseline_data = self.get_baseline_data()
        self.calculator = CropResidueCalculator(self.baseline_data)

    def validate_mode_data_compatibility(self):
        """
        Checks that the length of arrays in data matches the expected length for
        the selected mode. Raises an error or warning if there is a mismatch.
        """
        all_single_value = True

        for data_group in self.target_data_group:
            params = self.data[data_group]
            for values in params.values():
                if isinstance(values, np.ndarray) and len(values) > 1:
                    all_single_value = False
                    break

        if self.mode == "scientific" and all_single_value:
            warnings.warn(
                "All parameters have only one value. Switching to farmer mode.",
                UserWarning,
            )
            self.mode = "farmer"  # Change mode to farmer

        for data_group in self.target_data_group:
            params = self.data[data_group]
            for values in params.values():
                if isinstance(values, np.ndarray):
                    if self.mode == "farmer" and len(values) != 1:
                        raise ValueError(
                            "Length of the parameters should be 1 for farmer mode."
                        )
                    elif self.mode == "scientific" and len(values) < 1:
                        raise ValueError(
                            "Length of the parameters should be longer than 1 for scientific mode."
                        )

    def get_baseline_data(self):
        """
        Creates baseline data by taking the first element of each numpy array in nested
        dictionaries.  Specifically, extracts 'area' and 'yield' from 'farm_data' and the
        first element from 'crop_group_params' and 'crop_parameters'.
        """
        baseline = {}
        farm_data = self.data.get("farm_data", {})
        baseline["farm_data"] = {
            "area": farm_data.get("area", np.array([None]))[0],
            "yield": farm_data.get("yield", np.array([None]))[0],
        }

        for key, value in farm_data.items():
            if key not in ["area", "yield"]:
                if isinstance(value, np.ndarray):
                    baseline["farm_data"][key] = value[0]
                else:
                    baseline["farm_data"][key] = value

        for data_group in self.target_data_group:
            if data_group in self.data:
                params = self.data[data_group]
                baseline[data_group] = {}
                for parameter, value in params.items():
                    if isinstance(value, np.ndarray):
                        baseline[data_group][parameter] = value[0]
                    else:
                        baseline[data_group][parameter] = value

        return baseline

    def crop_analysis(self):
        """
        Determines calculation mode and executes accordingly.

        Returns
        -------
        dict
            A dictionary containing the results of the crop residue calculations.
        """
        if self.mode == "farmer":
            return self.farmer_mode()
        elif self.mode == "scientific":
            return self.scientific_mode()

    def farmer_mode(self):
        """
        Handles the 'farmer' mode where only a single set of calculations based on
        the baseline data is needed.

        Returns
        -------
        dict
            A dictionary containing the results for 'farmer' mode calculations.
        """
        results = {}
        calculator = CropResidueCalculator(self.baseline_data)
        results["C_p"] = np.array([calculator.c_p()])
        results["above_ground_carbon_input"] = np.array(
            [calculator.above_ground_carbon_input()]
        )
        results["below_ground_carbon_input"] = np.array(
            [calculator.below_ground_carbon_input()]
        )
        results["above_ground_residue_n"] = np.array(
            [calculator.above_ground_residue_n()]
        )
        results["below_ground_residue_n"] = np.array(
            [calculator.below_ground_residue_n()]
        )
        results["n_crop_residue"] = np.array([calculator.n_crop_residue()])
        return results

    def scientific_mode(self):
        """
        Handles the 'scientific' mode where variations for parameters with more than
        one value are calculated.

        Returns
        -------
        dict
            A dictionary containing the results for 'scientific' mode calculations.
        """
        results = {}
        target_data_group = ["crop_group_params", "crop_parameters"]

        for data_group in target_data_group:
            params = self.data[data_group]
            for parameter, values in params.items():
                if isinstance(values, np.ndarray):
                    cp_list = []
                    agci_list = []
                    bgci_list = []
                    agrn_list = []
                    bgrn_list = []
                    ncr_list = []

                    for value in values:
                        temp_data = copy.deepcopy(self.baseline_data)
                        temp_data[data_group][parameter] = value
                        calculator = CropResidueCalculator(temp_data)
                        cp_list.append(calculator.c_p())
                        agci_list.append(calculator.above_ground_carbon_input())
                        bgci_list.append(calculator.below_ground_carbon_input())
                        agrn_list.append(calculator.above_ground_residue_n())
                        bgrn_list.append(calculator.below_ground_residue_n())
                        ncr_list.append(calculator.n_crop_residue())

                    results[parameter] = {
                        "C_p": np.array(cp_list),
                        "above_ground_carbon_input": np.array(agci_list),
                        "below_ground_carbon_input": np.array(bgci_list),
                        "above_ground_residue_n": np.array(agrn_list),
                        "below_ground_residue_n": np.array(bgrn_list),
                        "n_crop_residue": np.array(ncr_list),
                    }
        return results


if __name__ == "__main__":

    #  Example usage of the CropResidueAggregator
    data_farm = {
        "farm_data": {
            "area": np.array([0.1409]),
            "latitude": np.array([46.4761852]),
            "longitude": np.array([-71.5189528]),
            "crop": np.array(["Soybean"], dtype="<U7"),
            "yield": np.array([2700.0]),
            "start_year": np.array([2021]),
            "end_year": np.array([2021]),
            "province": np.array(["Quebec"], dtype="<U6"),
            "group": np.array(["annual"]),
        },
        "crop_group_params": {
            "carbon_concentration": np.array([0.45]),
            "S_s": np.array([100.0]),
            "S_r": np.array([100.0]),
            "S_p": np.array([2.0]),
        },
        "crop_parameters": {
            "moisture": np.array([14.0]),
            "R_p": np.array([0.304]),
            "R_s": np.array([0.455]),
            "R_r": np.array([0.146]),
            "R_e": np.array([0.095]),
            "N_p": np.array([67.0]),
            "N_s": np.array([6.0]),
            "N_r": np.array([10.0]),
            "N_e": np.array([10.0]),
        },
        "climate_data": {
            "P": np.array([652.0]),
            "PE": np.array([556.0]),
            "FR_Topo": np.array([11.71]),
            "locations": np.array([[-71.5189528, 46.4761852]]),
            "soil_texture": np.array([0.49]),
        },
        "modifiers": {
            "RF_AM": np.array([1.0]),
            "RF_CS": np.array([1.0]),
            "RF_NS": np.array([0.84]),
            "RF_Till": np.array([1.0]),
        },
    }
    data_sci = {
        "farm_data": {
            "area": np.array([0.1409]),
            "latitude": np.array([46.4761852]),
            "longitude": np.array([-71.5189528]),
            "crop": np.array(["Soybean"], dtype="<U7"),
            "yield": np.array([2700.0]),
            "start_year": np.array([2021]),
            "end_year": np.array([2021]),
            "province": np.array(["Quebec"], dtype="<U6"),
            "group": np.array(["annual"]),
        },
        "crop_group_params": {
            "carbon_concentration": np.array([0.45, 0.50, 0.55]),
            "S_s": np.array([100.0, 105.0, 110.0]),
            "S_r": np.array([100.0, 105.0, 110.0]),
            "S_p": np.array([2.0, 2.5, 3.0]),
        },
        "crop_parameters": {
            "moisture": np.array([14.0, 15.0, 16.0]),
            "R_p": np.array([0.304, 0.314, 0.324]),
            "R_s": np.array([0.455, 0.465, 0.475]),
            "R_r": np.array([0.146, 0.156, 0.166]),
            "R_e": np.array([0.095, 0.105, 0.115]),
            "N_p": np.array([67.0, 70.0, 73.0]),
            "N_s": np.array([6.0, 7.0, 8.0]),
            "N_r": np.array([10.0, 11.0, 12.0]),
            "N_e": np.array([10.0, 11.0, 12.0]),
        },
        "climate_data": {
            "P": np.array([652.0]),
            "PE": np.array([556.0]),
            "FR_Topo": np.array([11.71]),
            "locations": np.array([[-71.5189528, 46.4761852]]),
            "soil_texture": np.array([0.49]),
        },
        "modifiers": {
            "RF_AM": np.array([1.0]),
            "RF_CS": np.array([1.0]),
            "RF_NS": np.array([0.84]),
            "RF_Till": np.array([1.0]),
        },
    }

    sci_calc1 = CropResidueAggregator(data_farm, "farmer")
    print("Results of Farmer Mode:")
    print(sci_calc1.crop_analysis())
    print("#" * 50)
    print("\n" * 2)
    sci_calc2 = CropResidueAggregator(data_farm, "scientific")
    print("Results of Scientific Mode with length 1:")
    print(sci_calc2.crop_analysis())
    print("#" * 50)
    print("\n" * 2)
    sci_calc3 = CropResidueAggregator(data_sci, "scientific")
    print("Results of Scientific Mode:")
    results = sci_calc3.crop_analysis()
    for key, value in results.items():
        print(key, value)
        print("\n")
