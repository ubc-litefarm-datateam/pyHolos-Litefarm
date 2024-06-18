import numpy as np
from emission_factor_calculator import EmissionFactorCalculator


class EmissionFactorAggregator:
    """
    A class to perform sensitivity analysis on emission factors.

    Parameters
    ----------
    farm_data : dict
        Contains all necessary climate data and modifiers for the given farm.
    operation_mode : str, optional
        Operation mode which can be 'farmer' for simplified outputs or 'scientific' for
        detailed analysis. Defaults to 'farmer'.

    Attributes
    ----------
    farm_data : dict
        Contains all necessary climate data and modifiers for the given farm.
    variables : list
        List of variables derived from climate data and modifiers for sensitivity analysis.
    mode : str
        Operation mode which can be 'farmer' for simplified outputs or 'scientific' for
        detailed analysis.
    results : dict
        Stores the sensitivity analysis results for each variable, structured by emission
        factor types.
    output : dict
        Final output depending on the operation mode.

    Methods
    -------
    perform_analysis()
        Performs sensitivity analysis for each variable in the variables list by merging and
        analyzing climate and modifier data.
    get_result()
        Compiles and returns results based on the operation mode.
    prepare_data_for_efc(selected_variable, value)
        Prepares farm data and a specific variable used for emission factor calculation.
    """

    def __init__(self, farm_data, operation_mode="farmer"):
        """
        Initializes the SensitivityEmissionFactor with provided farm data and operation mode.
        """
        self.farm_data = farm_data
        self.variables = [
            x
            for x in list(farm_data["climate_data"].keys())
            + list(farm_data["modifiers"].keys())
            if x not in ["locations"]
        ]
        self.mode = operation_mode
        self.results = {}
        self.output = {}

    def perform_analysis(self):
        """
        Performs sensitivity analysis for each variable in the variables list by merging and
        analyzing climate and modifier data.

        Returns
        -------
        dict
            A dictionary containing results of emission factor calculations for each variable.
        """
        # Iterating over all variables
        for variable in self.variables:
            # Initialize dictionary for each variable to store lists of results
            self.results[variable] = {}
            # Extract array values for the current variable
            # values_array = list(self.farm_data['climate_data'].get(variable, [])) + list(self.farm_data['modifiers'].get(variable, []))
            climate_data = np.array(self.farm_data["climate_data"].get(variable, []))
            modifiers = np.array(self.farm_data["modifiers"].get(variable, []))
            if climate_data.size == 0 and modifiers.size == 0:
                values_array = np.array([])  # Both are empty
            elif climate_data.size == 0:
                values_array = modifiers  # Only modifiers is non-empty
            elif modifiers.size == 0:
                values_array = climate_data  # Only climate data is non-empty
            else:
                values_array = np.concatenate(
                    (climate_data, modifiers)
                )  # Both are non-empty

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
        """
        Compiles and returns results based on the operation mode.
        If mode is 'farmer', only returns unnested results.

        Returns
        -------
        dict
            The result of the analysis according to the specified mode.
        """
        output_temp = self.perform_analysis()
        if self.mode == "farmer":
            self.output = output_temp[
                "P"
            ]  # All dictionary values are the same, can select other keys
        elif self.mode == "scientific":
            self.output = output_temp

        return self.output

    def prepare_data_for_efc(self, selected_variable, value):
        """
        Prepares farm data and a specific variable used for emission factor calculation.

        Parameters
        ----------
        selected_variable : str
            The variable to modify in the data set.
        value : float
            The new value for the selected variable.

        Returns
        -------
        dict
            Modified farm data with updated values for the selected variable.
        """
        data = {"climate_data": {}, "modifiers": {}}
        # Initialize all variables with their default values
        for var in self.variables:
            if var in self.farm_data["climate_data"]:
                data["climate_data"][var] = self.farm_data["climate_data"][var][0]
            if var in self.farm_data["modifiers"]:
                data["modifiers"][var] = self.farm_data["modifiers"][var][0]

        # Replace the value of the selected variable with the current value from its array
        if selected_variable in data["climate_data"]:
            data["climate_data"][selected_variable] = value
        elif selected_variable in data["modifiers"]:
            data["modifiers"][selected_variable] = value

        return data


if __name__ == "__main__":
    all_data_farmer = {
        "farm_data": {
            "area": np.array([0.1409]),
            "latitude": np.array([46.4761852]),
            "longitude": np.array([-71.5189528]),
            "crop": np.array(["Soybean"], dtype="<U7"),
            "yield": np.array([2700.0]),
            "start_year": np.array([2021]),
            "end_year": np.array([2021]),
            "province": np.array(["Quebec"], dtype="<U6"),
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

    all_data_sci = {
        "farm_data": {
            "area": np.array([0.1409, 0.2409, 0.3409]),
            "latitude": np.array([46.4761852, 46.4761852, 46.4761852]),
            "longitude": np.array([-71.5189528, -71.5189528, -71.5189528]),
            "crop": np.array(["Soybean", "Soybean", "Soybean"], dtype="<U7"),
            "yield": np.array([2700, 3700, 4700]),
            "start_year": np.array([2021, 2021, 2021]),
            "end_year": np.array([2021, 2021, 2021]),
            "province": np.array(["Quebec", "Quebec", "Quebec"], dtype="<U6"),
        },
        "crop_group_params": {
            "carbon_concentration": np.array([0.45, 0.55, 0.65]),
            "S_s": np.array([100, 50, 20]),
            "S_r": np.array([100, 50, 20]),
            "S_p": np.array([2, 5, 10]),
        },
        "crop_parameters": {
            "moisture": np.array([14, 17, 23]),
            "R_p": np.array([0.304, 0.404, 0.504]),
            "R_s": np.array([0.455, 0.555, 0.655]),
            "R_r": np.array([0.146, 0.246, 0.346]),
            "R_e": np.array([0.095, 0.195, 0.295]),
            "N_p": np.array([67, 77, 87]),
            "N_s": np.array([6, 8, 10]),
            "N_r": np.array([10, 12, 14]),
            "N_e": np.array([10, 12, 14]),
        },
        "climate_data": {
            "P": np.array([652, 752, 852]),
            "PE": np.array([556, 656, 756]),
            "FR_Topo": np.array([11.71, 22.71, 33.71]),
            "locations": np.array(
                [
                    [-71.5189528, 46.4761852],
                    [-71.5189528, 46.4761852],
                    [-71.5189528, 46.4761852],
                ]
            ),
            "soil_texture": np.array([0.49, 0.59, 0.69]),
        },
        "modifiers": {
            "RF_AM": np.array([1, 1, 1]),
            "RF_CS": np.array([1, 1, 1]),
            "RF_NS": np.array([0.84, 0.84, 0.84]),
            "RF_Till": np.array([1, 1, 1]),
        },
    }

    print("Farmers mode")
    sci_ef_calc = EmissionFactorAggregator(all_data_farmer)
    output = sci_ef_calc.get_result()
    print(output)
    print("-" * 50)
    print("\n" * 2)

    print("Scientific mode")
    sci_ef_calc = EmissionFactorAggregator(all_data_sci, operation_mode="scientific")
    output = sci_ef_calc.get_result()
    print(output)
    print("-" * 50)
    print("\n" * 2)
