import os
import json
import pandas as pd
import numpy as np


class CropParametersManager:
    """
    Extract crop-related parameters for specific crops under different climate conditions.

    Attributes
    ----------
    farm_data : dict
        Data about the farm including the type of crops grown in the farm.
    climate_data : dict
        Climate data including precipitation (P) and potential evapotranspiration (PE).
    crop : str
        Name of the crop.
    P : numpy.ndarray
        Precipitation data as a numpy array.
    PE : numpy.ndarray
        Potential evapotranspiration data as a numpy array.
    dir : str
        Directory path to the module's location.
    crop_parameters_path : str
        Path to the CSV file containing crop parameters.
    user_distributions_path : str
        Path to the JSON file containing user-defined distributions for crop parameters.
    crop_parameters : dict
        Stores parameters specific to the crop, formatted into a dictionary.

    Methods
    -------
    get_crop_parameters()
        Loads and filters crop parameters from the CSV file based on crop type and
        climate conditions.
    load_user_distributions()
        Loads user-defined distributions for the crop parameters from a JSON file.
    sample_crop_parameters(sampling_mode='default', num_samples=10)
        Samples crop parameters according to a specified mode, which can be 'default'
        for basic random sampling within the uniform range, or 'user_define' for
        user-defined distributions.

    Raises
    ------
    ValueError
        Raised if no user-defined distributions are found for the crop when 'user_define'
        sampling mode is selected or if an invalid sampling mode is specified.
    KeyError
        Raised if a parameter specified in the user-defined distributions does not exist
        in the crop parameters dictionary.
    """

    def __init__(self, farm_data, climate_data):
        """Initializes the class with farm and climate data."""
        self.farm_data = farm_data
        self.crop = self.farm_data["crop"]
        self.P = climate_data["P"][0]
        self.PE = climate_data["PE"][0]
        self.dir = os.path.dirname(__file__)
        self.crop_parameters_path = os.path.join(
            self.dir, "../../data/preprocessed/crop_parameters.csv"
        )
        self.user_distributions_path = os.path.join(
            self.dir, "../../data/params_sampling_range/crop_params_dist.json"
        )
        self.crop_parameters = self.get_crop_parameters()

    def get_crop_parameters(self):
        """
        Loads Holos crop parameters from a CSV file and filters them based on the
        specified crop and climate conditions.

        Returns
        -------
        dict
            A dictionary of crop parameters where keys are parameter names and values
            are numpy arrays containing the parameter values.
        """
        crop_params_df = pd.read_csv(self.crop_parameters_path)
        # Filter the dataframe for the given crop
        crop_params = crop_params_df[crop_params_df["crop"] == self.crop]

        # If only one row matches, return its parameters after cleaning
        if len(crop_params) == 1:
            selected_params = crop_params.iloc[0].to_dict()
            selected_params.pop("group", None)
            selected_params.pop("crop", None)
            selected_params.pop("condition", None)
            selected_params.pop("holos_crop_name", None)

            return {
                k: np.array([float(v)], dtype=np.float64)
                for k, v in selected_params.items()
            }

        selected_params = None  # This will store the selected row's dictionary

        # Process each row to find the best match according to the rules
        for _, row in crop_params.iterrows():
            condition = row["condition"]

            # Priority for 'Canada'
            if condition == "Canada":
                selected_params = row.to_dict()
                break  # Stop processing since 'Canada' has the highest priority

            # Handle 'irrigated' and 'rainfed' based on P and PE
            if self.P < self.PE and condition == "Irrigated":
                selected_params = row.to_dict()  # Prefer 'irrigated' if P < PE

            elif self.P >= self.PE and condition == "Rainfed":
                selected_params = row.to_dict()  # Prefer 'rainfed' otherwise

            # Handle numeric conditions with <, >, -
            elif "<" in condition:
                upper_bound = float(condition.replace("<", ""))
                if self.PE - self.P < upper_bound:
                    selected_params = row.to_dict()

            elif ">" in condition:
                lower_bound = float(condition.replace(">", ""))
                if self.PE - self.P > lower_bound:
                    selected_params = row.to_dict()

            elif "-" in condition:
                lower_bound, upper_bound = map(float, condition.split("-"))
                if lower_bound <= self.PE - self.P <= upper_bound:
                    selected_params = row.to_dict()

        if selected_params:
            # Clean up unnecessary data from the selected parameters
            selected_params.pop("group", None)
            selected_params.pop("crop", None)
            selected_params.pop("condition", None)
            selected_params.pop("holos_crop_name", None)

        return {
            k: np.array([float(v)], dtype=np.float64)
            for k, v in selected_params.items()
        }

    def load_user_distributions(self):
        """
        Loads user-defined distributions for crop parameters from a JSON file.

        Returns
        -------
        dict
            A dictionary containing the distributions, where each key is a parameter name
            and the value is a list defining the distribution type and parameters.
        """
        with open(self.user_distributions_path, "r") as file:
            return json.load(file)

    def sample_crop_parameters(self, sampling_mode="default", num_samples=10):
        """
        Samples crop parameters based on a specified mode ('default' or 'user_define') and
        number of samples.

        Parameters
        ----------
        sampling_mode : str, optional
            The mode to use for sampling, either 'default' or 'user_define'.
        num_samples : int, optional
            The number of samples to generate for each parameter.

        Returns
        -------
        dict
            A dictionary with sampled parameters where each key corresponds to a parameter
            name and the value is a numpy array containing the sampled values, with the
            original parameter value always at index 0.

        Raises
        ------
        ValueError
            If the specified sampling mode is invalid or if no user-defined distributions
            are available for 'user_define' mode.
        KeyError
            If a parameter in user-defined distributions is not found in the crop parameters.
        """
        sampled_parameters = {}
        if sampling_mode == "default":
            for param, value in self.crop_parameters.items():
                value = value[0]
                sampled_array = np.random.uniform(
                    value * 0.75, value * 1.25, num_samples
                )
                sampled_parameters[param] = np.insert(sampled_array, 0, value)
        elif sampling_mode == "user_define":
            user_distribution_dict = self.load_user_distributions()

            if user_distribution_dict is None:
                raise ValueError(
                    f"No user-defined distributions found for the crop '{self.crop}'."
                )

            user_distributions = user_distribution_dict.get(self.crop, None)
            if user_distributions is None:
                raise ValueError(
                    f"No user-defined distributions found for the crop '{self.crop}'."
                )

            for param, specs in user_distributions.items():
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
                # Add more distribution types as needed in future
                value = self.crop_parameters[param][0]
                sampled_parameters[param] = np.insert(sampled_array, 0, value)
        else:
            raise ValueError("Invalid sampling mode specified.")

        return sampled_parameters


# Usage example
if __name__ == "__main__":
    # Example farm and climate data setup for testing
    test_farm_data = {"crop": "Oats"}

    test_climate_data = {"P": np.array([100]), "PE": np.array([120])}

    # Initialize the CropParametersManager with the example data
    manager = CropParametersManager(test_farm_data, test_climate_data)

    # Fetch and print the crop parameters
    crop_parameters = manager.crop_parameters
    print("Crop Parameters:", crop_parameters)
    print(crop_parameters["moisture"].dtype)

    # Sample parameters with default settings
    default_samples = manager.sample_crop_parameters()
    print("Default Sampled Parameters:", default_samples)

    # Sample parameters with user-defined settings
    test_sampled_parameters = manager.sample_crop_parameters(
        sampling_mode="user_define"
    )
    print("Sampled Parameters:", test_sampled_parameters)
