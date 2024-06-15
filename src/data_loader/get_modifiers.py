import os
import json
import numpy as np
import pandas as pd

# import geopandas as gpd


class ModifiersManager:
    """
    Manages the retrieval and sampling of modifiers (reduction factors) for
    farming practices based on crop planted and the region the farm is located in.

    Attributes
    ----------
    farm_data : dict
        Dictionary containing data about the farm, including the province.
    rf_am : str
        Reduction factor of application method, defaults to "default".
    rf_cs : str
        Reduction factor for cropping systems, defaults to "Annual".
    rf_ns : str
        Reduction factor for nitrogen source, defaults to crop residue nitrogen,
        i.e.,"RF_NS_CRN".
    tillage : str
        Tillage modifier, i.e., conservation or conventional tillage, defaults to "unknown".
    dir : str
        Directory path to the module's location.
    modifiers : dict
        Dictionary containing the reduction factors, RF_*, as NumPy arrays.
    user_distributions_path : str
        Path to the JSON file containing user-defined distributions for sampling modifiers.

    Methods
    -------
    get_modifiers()
        Retrieves the modification factors based on the farm's region ('western_canada'
        or 'eastern_canada') and specific farming practices.
    get_region()
        Determines the region of the farm based on its province, categorizing as
        'western_canada' or 'eastern_canada'.
    load_user_distributions()
        Loads user-defined distributions for the reduction factors RF_* from a JSON file.
    sample_modifiers(sampling_mode='default', num_samples=10)
        Samples the reduction factors based on a specified mode (i.e., "default": Holos default
        values from pre-defined CSV files, "user-define": user-defined ranges, which can be
        loaded by load_user_distributions()) and number of samples.

    Raises
    ------
    ValueError
        If the sampling mode is 'user_define' but no user-defined distributions are found
        or if an invalid sampling mode is specified.
    KeyError
        If a parameter key is missing in the user-defined distributions when sampling in
        'user_define' mode.
    """

    def __init__(
        self,
        farm_data,
        rf_am="default",
        rf_cs="Annual",
        rf_ns="RF_NS_CRN",
        tillage="unknown",
    ):
        """Initializes the Modifiers object with farm data."""
        self.farm_data = farm_data
        self.rf_am = rf_am
        self.rf_cs = rf_cs
        self.rf_ns = rf_ns
        self.tillage = tillage
        self.dir = os.path.dirname(__file__)
        self.modifiers = self.get_modifiers()
        self.user_distributions_path = os.path.join(
            self.dir, "../../data/params_sampling_range/rf_params_dist.json"
        )

    def get_modifiers(self):
        """
        Retrieves reduction factors from CSV files based on the farm's practices and region.
        The values defined in these CSV files are defined in Holos.

        Returns
        -------
        dict
            A dictionary of reduction factors where each key is a modifier and each value
            is a NumPy array.
        """
        region = self.get_region()
        modifiers = {}
        # Define the list of modifiers and the relevant files
        modifier_files = {
            "RF_AM": "modifier_rf_am.csv",
            "RF_CS": "modifier_rf_cs.csv",
            "RF_NS": "modifier_rf_ns.csv",
            "RF_Till": "modifier_rf_till.csv",
        }

        # Iterate over the modifier files, loading and querying as needed
        for key, filename in modifier_files.items():
            path = os.path.join(self.dir, f"../../data/preprocessed/{filename}")
            df = pd.read_csv(path)

            if key == "RF_AM":
                value = float(df.query(f"method == '{self.rf_am}'")["value"].iloc[0])
            elif key == "RF_CS":
                value = float(df.query(f"group == '{self.rf_cs}'")["value"].iloc[0])
            elif key == "RF_NS":
                value = float(df.query(f"N_source == '{self.rf_ns}'")["value"].iloc[0])
            elif key == "RF_Till":
                value = float(
                    df.query(f"region == '{region}' & tillage == '{self.tillage}'")[
                        "value"
                    ].iloc[0]
                )

            modifiers[key] = value

        return {k: np.array([v]) for k, v in modifiers.items()}

    def get_region(self):
        """
        Determines the region based on the province information in farm_data.

        Returns
        -------
        str
            The region of the farm categorized as either 'western_canada' or 'eastern_canada'.
        """
        province = self.farm_data["province"]
        western_canada = [
            "Alberta",
            "British Columbia",
            "Manitoba",
            "Saskatchewan",
            "Northwest Territories",
            "Nunavut",
        ]

        return "western_canada" if province in western_canada else "eastern_canada"

    def load_user_distributions(self):
        """
        Loads the user-defined distributions for reduction factors from a JSON file
        specified by `user_distributions_path`.

        Returns
        -------
        dict
            A dictionary containing the user-defined distributions for each modifier (
            reduction factor, RF_*).
        """
        with open(self.user_distributions_path, "r") as file:
            return json.load(file)

    def sample_modifiers(self, sampling_mode="default", num_samples=10):
        """
        Samples reduction factors based on the provided mode and number of samples.

        Parameters
        ----------
        sampling_mode : str, optional
            The mode of sampling ('default' or 'user_define'), by default using 'default'.
            - "default": using Holos default values from pre-defined CSV files
            - "user-define": user-defined ranges, which is loaded by load_user_distributions()
        num_samples : int, optional
            The number of samples to generate for each factor, by default 10.

        Returns
        -------
        dict
            A dictionary with sampled parameters, where each entry contains an array of sampled 
            values for a parameter, starting with the original value.
        """
        sampled_parameters = {}

        # Load user distributions only if the sampling mode is 'user_define'
        if sampling_mode == "user_define":
            user_distributions = self.load_user_distributions()
            if user_distributions is None:
                raise ValueError("No user-defined RF distributions found.")
        else:
            user_distributions = None

        for param, value in self.modifiers.items():
            if sampling_mode == "default":
                sampled_array = np.random.uniform(
                    value * 0.75, value * 1.25, num_samples
                )
                sampled_parameters[param] = np.insert(sampled_array, 0, value)
            elif sampling_mode == "user_define":
                specs = user_distributions[param]
                if specs:
                    distribution_type = specs[0]
                    if distribution_type == "uniform":
                        low, high = specs[1], specs[2]
                        sampled_array = np.random.uniform(low, high, num_samples)
                    elif distribution_type == "normal":
                        mean, sd = specs[1], specs[2]
                        sampled_array = np.random.normal(mean, sd, num_samples)
                    elif distribution_type == "lognormal":
                        mean, sigma = specs[1], specs[2]
                        sampled_array = np.random.lognormal(mean, sigma, num_samples)
                    sampled_parameters[param] = np.insert(sampled_array, 0, value)
                else:
                    raise KeyError(f"Parameter '{param}' not found in RF parameters.")
            else:
                raise ValueError(
                    "Invalid sampling mode specified or undefined user distributions."
                )

        return sampled_parameters


# Example usage
if __name__ == "__main__":
    test_farm_data = {"province": "Alberta"}
    mod = ModifiersManager(test_farm_data)
    print("Calculated Modifiers:", mod.modifiers)

    default_samples = mod.sample_modifiers()
    print("Default Sampled Modifiers:", default_samples)

    try:
        user_defined_samples = mod.sample_modifiers(sampling_mode="user_define")
        print("User-defined Sampled Modifiers:", user_defined_samples)
    except ValueError as e:
        print(e)
