import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.calculator.emission_calculator import EmissionCalculator


class EmissionAggregator:
    """
    A class designed to perform sensitivity analysis on emissions influenced by
    both emission factors and nitrogen data.

    Parameters
    ----------
    ef_data : dict
        The emission factor data.
    n_data : dict
        The nitrogen-related data.
    operation_mode : str, optional
        Mode of operation, can be 'farmer' for simplified outputs or 'scientific' for detailed analysis.
        Defaults to 'farmer'.

    Attributes
    ----------
    ef_data : dict
        Contains emission factor data for different variables.
    n_data : dict
        Contains nitrogen data for different variables.
    variables : list
        List of variables derived from ef_data and n_data for conducting sensitivity analysis.
    mode : str
        Operation mode which can be 'farmer' for simplified outputs or 'scientific' for detailed analysis.
    results : dict
        Stores the detailed results of the analysis for each variable.
    output : dict
        Stores the final output depending on the operation mode.

    Methods
    -------
    perform_analysis()
        Performs a sensitivity analysis on emission across specified variables in the variables list.
    get_result()
        Returns the analyzed results according to the specified mode.
    prepare_ef_input_for_ec(selected_variable, value)
        Prepares the emission factor data for an emission calculation for a selected variable.
    prepare_n_input_for_ec(selected_variable, value)
        Prepares the nitrogen data for an emission calculation for a selected variable.
    """

    def __init__(self, ef_data, n_data, operation_mode="farmer"):
        """
        Initializes EmissionAggregator with emission factor data, nitrogen data,
        and an operation mode.
        """
        self.ef_data = ef_data
        self.n_data = n_data
        self.variables = list(ef_data.keys()) + list(n_data.keys())
        self.mode = operation_mode
        self.results = {}
        self.output = {}

    def perform_analysis(self):
        """
        Performs a sensitivity analysis on emission across specified variables in the variables list.

        Returns
        -------
        dict
            The computed results for each variable, structured by different types of emission outcomes.
        """
        # Iterating over all variables
        for variable in self.variables:
            # Initialize dictionary for each variable to store lists of results
            self.results[variable] = {}
            if self.mode == "farmer":
                if variable in self.ef_data.keys():
                    values_array = self.ef_data.get("EF")
                elif variable in self.n_data.keys():
                    values_array = self.n_data.get("n_crop_residue")
            # Extract array values for the current variable
            elif self.mode == "scientific":
                if variable in self.ef_data.keys():
                    values_array = self.ef_data.get(variable).get("EF")
                elif variable in self.n_data.keys():
                    values_array = self.n_data.get(variable).get("n_crop_residue")

            # Initialize results storage for this variable
            init_dict = {}
            for index in range(len(values_array)):
                modified_ef = self.prepare_ef_input_for_ec(
                    variable, values_array[index]
                )
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
        """
        Returns the analyzed results according to the specified mode. If mode is 'farmer',
        only returns unnested results.

        Returns
        -------
        dict
            The result of the analysis based on the specified mode.
        """
        output_temp = self.perform_analysis()
        if self.mode == "farmer":
            self.output = output_temp[
                "EF"
            ]  # All dictionary values are the same, can select other keys
        elif self.mode == "scientific":
            self.output = output_temp

        return self.output

    def prepare_ef_input_for_ec(self, selected_variable, value):
        """
        Prepares the input for an emission calculation by adjusting the emission factor
        for a selected variable.

        Parameters
        ----------
        selected_variable : str
            The variable to adjust in the emission factor data.
        value : float
            The new value to set for the emission factor.

        Returns
        -------
        dict
            The prepared emission factor data for the selected variable.
        """
        if self.mode == "farmer":
            ef_input = {"EF": self.ef_data.get("EF")[0]}
        elif self.mode == "scientific":
            ef_input = {"EF": self.ef_data.get("P").get("EF")[0]}

        if selected_variable in self.ef_data:
            ef_input["EF"] = value
        return ef_input

    def prepare_n_input_for_ec(self, selected_variable, value):
        """
        Prepares the input for an emission calculation by adjusting the nitrogen data for a selected variable.

        Parameters
        ----------
        selected_variable : str
            The variable to adjust in the nitrogen data.
        value : float
            The new value to set for the nitrogen parameter.

        Returns
        -------
        dict
            The prepared nitrogen data for the selected variable.
        """
        if self.mode == "farmer":
            n_input = {"n_crop_residue": self.n_data.get("n_crop_residue")[0]}
        if self.mode == "scientific":
            n_input = {
                "n_crop_residue": self.n_data.get("moisture").get("n_crop_residue")[0]
            }

        if selected_variable in self.n_data:
            n_input["n_crop_residue"] = value
        return n_input


if __name__ == "__main__":
    ef_data_farmer = {
        "EF_CT_P": np.array([0.01721731]),
        "EF_CT_PE": np.array([0.0100768]),
        "EF_Topo": np.array([0.01721731]),
        "EF": np.array([0.01098705]),
    }
    ef_data_scientific = {
        "P": {
            "EF_CT_P": np.array([0.01721731, 0.03008165, 0.05255789]),
            "EF_CT_PE": np.array([0.0100768, 0.0100768, 0.0100768]),
            "EF_Topo": np.array([0.01721731, 0.03008165, 0.05255789]),
            "EF": np.array([0.01098705, 0.01919629, 0.03353927]),
        },
        "PE": {
            "EF_CT_P": np.array([0.01721731, 0.01721731, 0.01721731]),
            "EF_CT_PE": np.array([0.0100768, 0.01760592, 0.03076062]),
            "EF_Topo": np.array([0.01721731, 0.01726282, 0.01880323]),
            "EF": np.array([0.01098705, 0.01101609, 0.01199909]),
        },
        "FR_Topo": {
            "EF_CT_P": np.array([0.01721731, 0.01721731, 0.01721731]),
            "EF_CT_PE": np.array([0.0100768, 0.0100768, 0.0100768]),
            "EF_Topo": np.array([0.01721731, 0.01721731, 0.01721731]),
            "EF": np.array([0.01098705, 0.01098705, 0.01098705]),
        },
        "soil_texture": {
            "EF_CT_P": np.array([0.01721731, 0.01721731, 0.01721731]),
            "EF_CT_PE": np.array([0.0100768, 0.0100768, 0.0100768]),
            "EF_Topo": np.array([0.01721731, 0.01721731, 0.01721731]),
            "EF": np.array([0.01098705, 0.0132293, 0.01547155]),
        },
        "RF_AM": {
            "EF_CT_P": np.array([0.01721731, 0.01721731, 0.01721731]),
            "EF_CT_PE": np.array([0.0100768, 0.0100768, 0.0100768]),
            "EF_Topo": np.array([0.01721731, 0.01721731, 0.01721731]),
            "EF": np.array([0.01098705, 0.01098705, 0.01098705]),
        },
        "RF_CS": {
            "EF_CT_P": np.array([0.01721731, 0.01721731, 0.01721731]),
            "EF_CT_PE": np.array([0.0100768, 0.0100768, 0.0100768]),
            "EF_Topo": np.array([0.01721731, 0.01721731, 0.01721731]),
            "EF": np.array([0.01098705, 0.01098705, 0.01098705]),
        },
        "RF_NS": {
            "EF_CT_P": np.array([0.01721731, 0.01721731, 0.01721731]),
            "EF_CT_PE": np.array([0.0100768, 0.0100768, 0.0100768]),
            "EF_Topo": np.array([0.01721731, 0.01721731, 0.01721731]),
            "EF": np.array([0.01098705, 0.01098705, 0.01098705]),
        },
        "RF_Till": {
            "EF_CT_P": np.array([0.01721731, 0.01721731, 0.01721731]),
            "EF_CT_PE": np.array([0.0100768, 0.0100768, 0.0100768]),
            "EF_Topo": np.array([0.01721731, 0.01721731, 0.01721731]),
            "EF": np.array([0.01098705, 0.01098705, 0.01098705]),
        },
    }

    n_data_farmer = {
        "C_p": np.array([3268.0]),
        "above_ground_carbon_input": np.array([5228.8]),
        "below_ground_carbon_input": np.array([1307.1999999999998]),
        "above_ground_residue_n": np.array([14.161333333333335]),
        "below_ground_residue_n": np.array([2.5417777777777775]),
        "n_crop_residue": np.array([1670.3111111111114]),
    }

    n_data_scientific = {
        "area": {
            "C_p": np.array([3268.0]),
            "above_ground_carbon_input": np.array([5228.8]),
            "below_ground_carbon_input": np.array([1307.1999999999998]),
            "above_ground_residue_n": np.array([14.161333333333335]),
            "below_ground_residue_n": np.array([2.5417777777777775]),
            "n_crop_residue": np.array([1670.3111111111114]),
        },
        "yield": {
            "C_p": np.array([3268.0]),
            "above_ground_carbon_input": np.array([5228.8]),
            "below_ground_carbon_input": np.array([1307.1999999999998]),
            "above_ground_residue_n": np.array([14.161333333333335]),
            "below_ground_residue_n": np.array([2.5417777777777775]),
            "n_crop_residue": np.array([1670.3111111111114]),
        },
        "group": {
            "C_p": np.array([3268.0, 3268.0, 3268.0]),
            "above_ground_carbon_input": np.array([5228.8, 5228.8, 5228.8]),
            "below_ground_carbon_input": np.array(
                [1307.1999999999998, 1307.1999999999998, 1307.1999999999998]
            ),
            "above_ground_residue_n": np.array(
                [14.161333333333335, 14.161333333333335, 6.5360000000000005]
            ),
            "below_ground_residue_n": np.array(
                [2.5417777777777775, 1.6703111111111109, 2.5417777777777775]
            ),
            "n_crop_residue": np.array(
                [1670.3111111111114, 1583.1644444444446, 907.7777777777777]
            ),
        },
        "S_p": {
            "C_p": np.array([3268.0, 3182.0, 3096.0]),
            "above_ground_carbon_input": np.array([5228.8, 4932.099999999999, 4644.0]),
            "below_ground_carbon_input": np.array(
                [1307.1999999999998, 1272.8, 1238.3999999999999]
            ),
            "above_ground_residue_n": np.array(
                [14.161333333333335, 13.435111111111109, 12.727999999999998]
            ),
            "below_ground_residue_n": np.array(
                [2.5417777777777775, 2.4748888888888887, 2.408]
            ),
            "n_crop_residue": np.array(
                [1670.3111111111114, 1590.9999999999995, 1513.5999999999997]
            ),
        },
        "S_s": {
            "C_p": np.array([3268.0, 3268.0, 3268.0]),
            "above_ground_carbon_input": np.array([5228.8, 5392.200000000001, 5555.6]),
            "below_ground_carbon_input": np.array(
                [1307.1999999999998, 1307.1999999999998, 1307.1999999999998]
            ),
            "above_ground_residue_n": np.array(
                [14.161333333333335, 14.706, 15.250666666666667]
            ),
            "below_ground_residue_n": np.array(
                [2.5417777777777775, 2.5417777777777775, 2.5417777777777775]
            ),
            "n_crop_residue": np.array(
                [1670.3111111111114, 1724.7777777777778, 1779.2444444444445]
            ),
        },
        "S_r": {
            "C_p": np.array([3268.0, 3268.0, 3268.0]),
            "above_ground_carbon_input": np.array([5228.8, 5228.8, 5228.8]),
            "below_ground_carbon_input": np.array([1307.1999999999998, 1388.9, 1470.6]),
            "above_ground_residue_n": np.array(
                [14.161333333333335, 14.161333333333335, 14.161333333333335]
            ),
            "below_ground_residue_n": np.array(
                [2.5417777777777775, 2.7233333333333336, 2.904888888888889]
            ),
            "n_crop_residue": np.array(
                [1670.3111111111114, 1688.4666666666667, 1706.6222222222223]
            ),
        },
        "carbon_concentration": {
            "C_p": np.array([3268.0, 4085.0, 4902.0]),
            "above_ground_carbon_input": np.array([5228.8, 6536.0, 7843.2]),
            "below_ground_carbon_input": np.array(
                [1307.1999999999998, 1634.0, 1960.7999999999997]
            ),
            "above_ground_residue_n": np.array(
                [14.161333333333335, 17.701666666666668, 21.241999999999997]
            ),
            "below_ground_residue_n": np.array(
                [2.5417777777777775, 3.1772222222222224, 3.8126666666666664]
            ),
            "n_crop_residue": np.array(
                [1670.3111111111114, 2087.888888888889, 2505.4666666666662]
            ),
        },
        "moisture": {
            "C_p": np.array([3268.0, 3230.0, 3192.0]),
            "above_ground_carbon_input": np.array([5228.8, 5168.0, 5107.2]),
            "below_ground_carbon_input": np.array([1307.1999999999998, 1292.0, 1276.8]),
            "above_ground_residue_n": np.array(
                [14.161333333333335, 13.996666666666666, 13.831999999999999]
            ),
            "below_ground_residue_n": np.array(
                [2.5417777777777775, 2.5122222222222224, 2.4826666666666664]
            ),
            "n_crop_residue": np.array(
                [1670.3111111111114, 1650.8888888888891, 1631.4666666666665]
            ),
        },
        "R_p": {
            "C_p": np.array([3268.0, 3268.0, 3268.0]),
            "above_ground_carbon_input": np.array([5228.8, 4085.0, 3703.7333333333336]),
            "below_ground_carbon_input": np.array(
                [1307.1999999999998, 653.5999999999999, 435.73333333333335]
            ),
            "above_ground_residue_n": np.array(
                [14.161333333333335, 10.348666666666666, 9.07777777777778]
            ),
            "below_ground_residue_n": np.array(
                [2.5417777777777775, 1.2708888888888887, 0.8472592592592594]
            ),
            "n_crop_residue": np.array(
                [1670.3111111111114, 1161.9555555555555, 992.5037037037038]
            ),
        },
        "R_s": {
            "C_p": np.array([3268.0, 3268.0, 3268.0]),
            "above_ground_carbon_input": np.array([5228.8, 6372.599999999999, 7516.4]),
            "below_ground_carbon_input": np.array(
                [1307.1999999999998, 1307.1999999999998, 1307.1999999999998]
            ),
            "above_ground_residue_n": np.array(
                [14.161333333333335, 17.973999999999997, 21.78666666666667]
            ),
            "below_ground_residue_n": np.array(
                [2.5417777777777775, 2.5417777777777775, 2.5417777777777775]
            ),
            "n_crop_residue": np.array(
                [1670.3111111111114, 2051.5777777777776, 2432.844444444445]
            ),
        },
        "R_r": {
            "C_p": np.array([3268.0, 3268.0, 3268.0]),
            "above_ground_carbon_input": np.array([5228.8, 5228.8, 5228.8]),
            "below_ground_carbon_input": np.array(
                [1307.1999999999998, 2287.6, 3267.999999999999]
            ),
            "above_ground_residue_n": np.array(
                [14.161333333333335, 14.161333333333335, 14.161333333333335]
            ),
            "below_ground_residue_n": np.array(
                [2.5417777777777775, 4.720444444444444, 6.89911111111111]
            ),
            "n_crop_residue": np.array(
                [1670.3111111111114, 1888.1777777777777, 2106.0444444444447]
            ),
        },
        "R_e": {
            "C_p": np.array([3268.0, 3268.0, 3268.0]),
            "above_ground_carbon_input": np.array([5228.8, 5228.8, 5228.8]),
            "below_ground_carbon_input": np.array([1307.1999999999998, 1634.0, 1960.8]),
            "above_ground_residue_n": np.array(
                [14.161333333333335, 14.161333333333335, 14.161333333333335]
            ),
            "below_ground_residue_n": np.array(
                [2.5417777777777775, 2.9048888888888884, 3.268]
            ),
            "n_crop_residue": np.array(
                [1670.3111111111114, 1706.6222222222223, 1742.9333333333336]
            ),
        },
        "N_p": {
            "C_p": np.array([3268.0, 3268.0, 3268.0]),
            "above_ground_carbon_input": np.array([5228.8, 5228.8, 5228.8]),
            "below_ground_carbon_input": np.array(
                [1307.1999999999998, 1307.1999999999998, 1307.1999999999998]
            ),
            "above_ground_residue_n": np.array(
                [14.161333333333335, 20.697333333333333, 27.233333333333334]
            ),
            "below_ground_residue_n": np.array(
                [2.5417777777777775, 2.5417777777777775, 2.5417777777777775]
            ),
            "n_crop_residue": np.array(
                [1670.3111111111114, 2323.911111111111, 2977.5111111111114]
            ),
        },
        "N_s": {
            "C_p": np.array([3268.0, 3268.0, 3268.0]),
            "above_ground_carbon_input": np.array([5228.8, 5228.8, 5228.8]),
            "below_ground_carbon_input": np.array(
                [1307.1999999999998, 1307.1999999999998, 1307.1999999999998]
            ),
            "above_ground_residue_n": np.array(
                [14.161333333333335, 19.24488888888889, 24.328444444444447]
            ),
            "below_ground_residue_n": np.array(
                [2.5417777777777775, 2.5417777777777775, 2.5417777777777775]
            ),
            "n_crop_residue": np.array(
                [1670.3111111111114, 2178.666666666667, 2687.0222222222224]
            ),
        },
        "N_r": {
            "C_p": np.array([3268.0, 3268.0, 3268.0]),
            "above_ground_carbon_input": np.array([5228.8, 5228.8, 5228.8]),
            "below_ground_carbon_input": np.array(
                [1307.1999999999998, 1307.1999999999998, 1307.1999999999998]
            ),
            "above_ground_residue_n": np.array(
                [14.161333333333335, 14.161333333333335, 14.161333333333335]
            ),
            "below_ground_residue_n": np.array(
                [2.5417777777777775, 3.6311111111111107, 4.720444444444444]
            ),
            "n_crop_residue": np.array(
                [1670.3111111111114, 1779.2444444444445, 1888.1777777777777]
            ),
        },
        "N_e": {
            "C_p": np.array([3268.0, 3268.0, 3268.0]),
            "above_ground_carbon_input": np.array([5228.8, 5228.8, 5228.8]),
            "below_ground_carbon_input": np.array(
                [1307.1999999999998, 1307.1999999999998, 1307.1999999999998]
            ),
            "above_ground_residue_n": np.array(
                [14.161333333333335, 14.161333333333335, 14.161333333333335]
            ),
            "below_ground_residue_n": np.array(
                [2.5417777777777775, 2.723333333333333, 2.9048888888888884]
            ),
            "n_crop_residue": np.array(
                [1670.3111111111114, 1688.4666666666667, 1706.6222222222223]
            ),
        },
    }

    print("Farmers mode")
    sci_emission_calc = EmissionAggregator(ef_data_farmer, n_data_farmer)
    output = sci_emission_calc.get_result()
    print(output)
    print("-" * 50)
    print("\n" * 2)

    print("Scientific mode")
    sci_emission_calc = EmissionAggregator(
        ef_data_scientific, n_data_scientific, operation_mode="scientific"
    )
    output = sci_emission_calc.get_result()
    print(output)
    print("-" * 50)
    print("\n" * 2)
