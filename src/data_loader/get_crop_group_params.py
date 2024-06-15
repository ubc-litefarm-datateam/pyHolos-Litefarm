import os
import json
import pandas as pd
import numpy as np


class CropGroupManager:
    """
    Manages the retrieval and sampling of crop group parameters based on the specific
    crop planted in the given farm.

    Parameters
    ----------
    farm_data : dict
        A dictionary containing information about the farm, specifically the crop name.

    Attributes
    ----------
    crop : str
        The crop planted in the given farm data.
    crop_group : str
        The group category to which the crop belongs, e.g., 'Annual', 'Silage',
        'Cover', 'Root', and 'Perennial'.
    crop_group_params : dict
        A dictionary of parameters associated with the crop group, including
        'carbon_concentration', 'S_s', 'S_r', and 'S_p'.
    user_distributions_path : str
        Path to the JSON file containing user-defined distributions for parameter sampling.

    Methods
    -------
    get_crop_group()
        Identifies the group for the crop from a predefined mapping in a CSV file.
    get_crop_group_parameters()
        Retrieves crop-group parameters for the identified crop group from a CSV file
        and stores them in a dictionary.
    load_user_distributions()
        Loads user-defined distributions for crop-group parameters from a JSON file.
    sample_crop_group_parameters(sampling_mode='default', num_samples=10)
        Samples parameters based on the specified mode and number of samples.

    Raises
    ------
    ValueError
        If the user-defined sampling mode is selected but no distributions are found
        for the crop group.
    KeyError
        If a parameter specified in the user-defined distributions does not exist in
        the crop group parameters.
    """

    def __init__(self, farm_data):
        """Initializes the CropGroupManager with the farm data provided."""
        self.farm_data = farm_data
        self.crop = self.farm_data["crop"]
        self.dir = os.path.dirname(__file__)
        self.crop_to_group_map_path = os.path.join(
            self.dir, "../../data/preprocessed/crop_to_group.csv"
        )
        self.crop_group_params_path = os.path.join(
            self.dir, "../../data/preprocessed/crop_group_parameters.csv"
        )
        self.user_distributions_path = os.path.join(
            self.dir, "../../data/params_sampling_range/crop_group_params_dist.json"
        )
        self.crop_group = self.get_crop_group()
        self.crop_group_params = self.get_crop_group_parameters()

    def get_crop_group(self):
        """
        Retrieves the group for the specified crop from a CSV mapping file.

        Returns
        -------
        str
            The group category of the crop.
        """
        crop_to_group_map_df = pd.read_csv(self.crop_to_group_map_path)
        crop_group = crop_to_group_map_df.query(f"crop == '{self.crop}'")["group"].iloc[
            0
        ]
        return crop_group

    def get_crop_group_parameters(self):
        """
        Retrieves and formats parameters specific to the crop group from a CSV file.

        Returns
        -------
        dict
            A dictionary where each key is a parameter name and each value is a
            NumPy array containing the parameter value.
        """
        crop_group_params_df = pd.read_csv(self.crop_group_params_path)
        crop_group_params = (
            crop_group_params_df[crop_group_params_df["group"] == self.crop_group]
            .iloc[0]
            .to_dict()
        )
        crop_group_params.pop("group", None)
        return {k: np.array([float(v)]) for k, v in crop_group_params.items()}

    def load_user_distributions(self):
        """
        Loads user-defined distributions from a JSON file for sampling parameters.

        Returns
        -------
        dict
            A dictionary containing the user-defined distributions.
        """
        with open(self.user_distributions_path, "r") as file:
            return json.load(file)

    def sample_crop_group_parameters(self, sampling_mode="default", num_samples=10):
        """
        Samples crop group parameters based on the specified mode and number of samples.

        Parameters
        ----------
        sampling_mode : str, optional
            The mode of sampling ('default' or 'user_define'), default is 'default'.
        num_samples : int, optional
            The number of samples to generate, default is 10.

        Returns
        -------
        dict
            A dictionary with sampled parameters. Each key corresponds to a parameter name,
            and the value is a NumPy array containing the sampled values, with the original
            value at index 0.

        Raises
        ------
        ValueError
            If no user-defined distributions are found for the crop group when 'user_define'
            mode is selected.
        KeyError
            If a parameter in the user-defined distributions does not exist in the current
            crop group parameters.
        """
        sampled_parameters = {}
        if sampling_mode == "default":
            for param, value in self.crop_group_params.items():
                sampled_array = np.random.uniform(
                    value * 0.75, value * 1.25, num_samples
                )
                sampled_parameters[param] = np.insert(sampled_array, 0, value)
        elif sampling_mode == "user_define":
            user_distribution_dict = self.load_user_distributions()

            if user_distribution_dict is None:
                raise ValueError(
                    f"No user-defined distributions found for the crop group '{self.crop_group}'."
                )

            user_distributions = user_distribution_dict.get(self.crop_group, None)
            if user_distributions is None:
                raise ValueError(
                    f"No user-defined distributions found for the crop group '{self.crop_group}'."
                )

            for param, specs in user_distributions.items():
                distribution_type = specs[0]
                # sampled_array = None
                if distribution_type == "uniform":
                    low, high = specs[1], specs[2]
                    sampled_array = np.random.uniform(low, high, num_samples)
                elif distribution_type == "normal":
                    mean, sd = specs[1], specs[2]
                    sampled_array = np.random.normal(mean, sd, num_samples)
                elif distribution_type == "lognormal":
                    mean, sigma = specs[1], specs[2]
                    sampled_array = np.random.lognormal(mean, sigma, num_samples)

                # Ensure the parameter exists in crop_group_params before attempting to access it
                if param in self.crop_group_params:
                    value = self.crop_group_params[param]
                    sampled_parameters[param] = np.insert(sampled_array, 0, value)
                else:
                    raise KeyError(
                        f"Parameter '{param}' not found in crop group parameters."
                    )
        else:
            raise ValueError(
                "Invalid sampling mode specified or undefined user distributions."
            )

        return sampled_parameters


# Example usage
if __name__ == "__main__":
    # Example farm_data containing 'crop' information
    test_farm_data = {"crop": "Wheat"}
    manager = CropGroupManager(test_farm_data)
    print("Crop Group Parameters:", manager.crop_group_params)

    default_samples = manager.sample_crop_group_parameters()
    print("Default Sampled Parameters:", default_samples)

    try:
        user_defined_samples = manager.sample_crop_group_parameters(
            sampling_mode="user_define"
        )
        print("User-defined Sampled Parameters:", user_defined_samples)
    except ValueError as e:
        print(e)
