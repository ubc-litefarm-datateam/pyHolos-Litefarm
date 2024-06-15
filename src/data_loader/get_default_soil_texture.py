"""
This module provides the ModifierSoilTexture class used to extract soil texture modifiers 
defined by Holos based on farm region (i.e., western/eastern Canana) and the soil texture 
(i.e., 'fine', 'medium', 'coarse') of the ecodistrict the farm is located in.
"""

import os
import pandas as pd


class ModifierSoilTexture:
    """
    Getting Holos RF_TX values: fetches soil texture values based on the
    ecodistrict-wide soil texture provided by Holos.

    Parameters
    ----------
    farm_data : dict
        A dictionary containing information about the farm, such as the province.
    soil_texture : str, optional
        The soil texture type. Default is 'unknown'.

    Attributes
    ----------
    farm_data : dict
        Store the farm data passed during initialization.
    province : str
        The province extracted from farm_data.
    soil_texture : str
        The soil texture type (i.e., 'fine', 'coarse', 'medium', 'unknown').
    dir : str
        The directory of the script that is running this class.
    soil_texture_path : str
        The path to the CSV file containing soil texture modifiers.
    rf_tx : float
        The fetched soil texture modifier based on the region and the
        specified soil texture.

    Methods
    -------
    get_rf_tx_modifier()
        Fetches the soil texture modifier from the CSV file based on the
        region and soil texture.
    get_region()
        Determines the region (western or eastern Canada) based on the province.

    Examples
    --------
    >>> farm_data = {'province': 'Quebec'}
    >>> soil_texture = 'fine'
    >>> modifier = ModifierSoilTexture(farm_data, soil_texture)
    >>> print(modifier.get_rf_tx_modifier())
    """

    def __init__(self, farm_data, soil_texture="unknown"):
        """
        Initialize the ModifierSoilTexture with required parameters.
        """
        self.farm_data = farm_data
        self.province = farm_data["province"]
        self.soil_texture = soil_texture
        self.dir = os.path.dirname(__file__)
        self.soil_texture_path = os.path.join(
            self.dir, "../../data/preprocessed/modifier_rf_tx.csv"
        )
        self.rf_tx = self.get_rf_tx_modifier()

    def get_rf_tx_modifier(self):
        """
        Fetches the soil texture modifier from the CSV file based on the
        determined region and the specified soil texture.

        Returns
        -------
        float
            The soil texture modifier value.

        Examples
        --------
        >>> test_farm_data = {'province': 'Quebec'}
        >>> test_soil_texture = 'fine'
        >>> modifier = ModifierSoilTexture(test_farm_data, test_soil_texture)
        >>> print(modifier.get_rf_tx_modifier())
        """
        region = self.get_region()
        soil_texture_df = pd.read_csv(self.soil_texture_path)
        rf_tx = soil_texture_df.query(
            f"region == '{region}' & soil_texture == '{self.soil_texture}'"
        )["value"].iloc[0]
        return rf_tx

    def get_region(self):
        """
        Determines the region based on the province specified in the farm data. 

        Returns
        -------
        str
            Returns 'western_canada' if the province is part of Western Canada 
            or 'eastern_canada' if not.

        Examples
        --------
        >>> farm_data = {'province': 'Quebec'}
        >>> modifier = ModifierSoilTexture(farm_data)
        >>> print(modifier.get_region())
        'eastern_canada'
        """
        western_canada = [
            "Alberta",
            "British Columbia",
            "Manitoba",
            "Saskatchewan",
            "Northwest Territories",
            "Nunavut",
        ]

        return "western_canada" if self.province in western_canada else "eastern_canada"


if __name__ == "__main__":
    # Example farm data
    test_farm_data = {
        "province": "Quebec",  # Province should be one that is recognized by your class
    }
    # Example soil texture
    test_soil_texture = (
        "fine"  # Soil texture should be one that is available in your CSV file
    )

    # Initialize the ModifierSoilTexture class with the example farm data and soil texture
    modifier = ModifierSoilTexture(test_farm_data, test_soil_texture)
    print(modifier.get_region())

    # Fetch and print the RF_TX modifier
    rf_tx_modifier = modifier.get_rf_tx_modifier()
    print(f"RF_TX Modifier for the region and soil texture: {rf_tx_modifier}")
