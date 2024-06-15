import os
import json
import rasterio
import pandas as pd
import numpy as np


class ExternalSoilTextureDataFetcher:
    """
    Fetches and maps soil texture data from the Harmonized World Soil Database v2.0
    to geographic points.
    See details in https://www.fao.org/soils-portal/data-hub/soil-maps-and-databases/harmonized-world-soil-database-v20/en/.

    Parameters
    ----------
    points : list of tuples
        List of (longitude, latitude) tuples for which soil texture data is required.

    Attributes
    ----------
    points : list of tuples
        Geographical points for soil data extraction.
    dir : str
        Base directory path for data files.
    smu_csv_path : str
        Path to the Soil Mapping Unit (SMU) CSV data file, 'HWSD2_SMU.csv', obtained from HSWD2.mdb.
    texture_csv_path : str
        Path to the USDA texture CSV data file, `D_TEXTURE_USDA.csv`, obtained from HSWD2.mdb.
    texture_mapped_path : str
        Path to the preprocessed mapped soil texture values CSV file.
    raster_path : str
        Path to the HWSD2 Raster 2.0 data file.
    src : rasterio.io.DatasetReader or None
        Active raster data source.

    Methods
    -------
    load_data()
        Loads necessary CSV data files into pandas dataframes.
    open_raster()
        Initializes the raster data file for reading.
    close_raster()
        Closes the active raster data source.
    get_raster_value(lon, lat)
        Retrieves the soil mapping unit ID (SMU_ID) at specified coordinates.
    lookup_soil_texture(smu_id)
        Returns the soil texture type associated with a soil mapping unit ID (SMU_ID).
    get_soil_texture_values()
        Fetches soil texture values for all specified points and returns them.

    Examples
    --------
    >>> points = [(34.0522, -118.2437), (36.7783, -119.4179)]
    >>> fetcher = ExternalSoilTextureDataFetcher(points)
    >>> soil_textures = fetcher.get_soil_texture()
    """

    def __init__(self, points):
        self.points = points
        self.dir = os.path.dirname(__file__)
        self.smu_csv_path = os.path.join(
            self.dir, "../../data/external/HWSD2/HWSD2_SMU.csv"
        )
        self.texture_csv_path = os.path.join(
            self.dir, "../../data/external/HWSD2/D_TEXTURE_USDA.csv"
        )
        self.raster_path = os.path.join(
            self.dir, "../../data/external/HWSD2_RASTER/HWSD2.bil"
        )
        self.texture_mapped_path = os.path.join(
            self.dir, "../../data/params_sampling_range/rf_tx_params_dist.json"
        )
        self.src = None
        self.load_data()

    def load_data(self):
        """
        Loads CSV data into pandas DataFrames, including soil mapping unit (SMU)
        data and texture classification data.
        """
        self.smu_df = pd.read_csv(self.smu_csv_path)
        self.texture_df = pd.read_csv(self.texture_csv_path)

    def load_user_rf_tx_distributions(self):
        """
        Loads user-defined distributions for soil texture parameters from a JSON file.

        Returns
        -------
        dict
            A dictionary containing the midpoint and range of soil texture parameters.
        """
        with open(self.texture_mapped_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def sampling_rf_tx(self, soil_type, first_point=False):
        """
        Randomly sample a soil texture value based on the provided soil type.

        Parameters
        ----------
        soil_type : str
            The soil type for which to sample texture parameters.
        first_point : bool, optional
            Whether to sample only the midpoint value (default is False).

        Returns
        -------
        float or np.nan
            The sampled texture value or NaN if the soil type is missing or invalid.

        Raises
        ------
        ValueError
            If no user-defined RF soil texture distributions are found.
        """
        rf_tx_distributions = self.load_user_rf_tx_distributions()
        if rf_tx_distributions is None:
            raise ValueError("No user-defined RF soil texture distributions found.")

        if soil_type == "missing texture type" or soil_type == "no matching SMU ID":
            return np.nan

        if first_point:
            return rf_tx_distributions["midpoint"].get(soil_type)

        low, high = rf_tx_distributions["range"].get(soil_type)
        sampled_rf_tx = np.random.uniform(low, high, 1)
        return sampled_rf_tx[0]

    def open_raster(self):
        """Opens the raster data file for geographical data extraction."""
        self.src = rasterio.open(self.raster_path)

    def close_raster(self):
        """Closes the open raster data file."""
        if self.src:
            self.src.close()

    def get_raster_value(self, lon, lat):
        """
        Retrieves the soil mapping unit id (SMU_ID) from the raster
        at specified geographic coordinates.

        Parameters
        ----------
        lon : float
            Longitude of the point.
        lat : float
            Latitude of the point.

        Returns
        ----------
        int
            The soil mapping unit id (SMU_ID) corresponding to the provided coordinates.
        """
        row, col = self.src.index(lon, lat)
        return self.src.read(1)[row, col]

    def lookup_soil_texture(self, smu_id):
        """
        Retrieves the soil texture type associated with a given SMU_ID.

        Parameters
        ----------
        smu_id : int
            The soil mapping unit id (SMU_ID).

        Returns
        ----------
        str
            The texture type if found; otherwise, a status string indicating the error.
        """
        # Query the texture code from the SMU DataFrame
        query_result = self.smu_df[self.smu_df["HWSD2_SMU_ID"] == smu_id][
            "TEXTURE_USDA"
        ]
        if not query_result.empty:
            texture_code = query_result.iloc[0]
            if not np.isnan(texture_code):
                texture_type = self.texture_df[self.texture_df["CODE"] == texture_code][
                    "VALUE"
                ].iloc[0]
                # print(f"The soil texture type for SMU_ID {smu_id} is {texture_type}.")
                return texture_type

            # print(f"No texture type found for SMU_ID {smu_id}: 'missing texture type'.")
            return "missing texture type"

        # print(f"No matching SMU_ID for the selected point: 'no matching SMU ID'.")
        return "no matching SMU ID"

    def get_soil_texture_values(self):
        """
        Retrieves and maps soil texture data for all specified geographic points.

        Returns
        ----------
        dict
            A dictionary mapping each point to its corresponding soil texture value.
        """
        self.open_raster()
        rf_tx_values = {}
        first_point = True
        for lon, lat in self.points:
            smu_id = self.get_raster_value(lon, lat)
            texture_type = self.lookup_soil_texture(smu_id)
            rf_tx = self.sampling_rf_tx(texture_type, first_point)
            rf_tx_values[(lon, lat)] = rf_tx
            first_point = False
        self.close_raster()

        return rf_tx_values


if __name__ == "__main__":
    # The first and second points have a match
    # The 3rd point, texture_type is missing. this is because in the database, there is no
    # USDA_TEXTURE entry for this SMU 7001 (soil mapping unit).
    # The 4th point is Vancouver Harbor, we don't have a valid SMU since it is water surface
    # HSWD2 has a high resolution 1km * 1km
    test_points = [
        (-93.6250, 42.0329),
        (-94.1110, 42.6329),
        (-89.3985, 43.0731),
        (-122.9618, 49.2957),
    ]
    soil_fetcher = ExternalSoilTextureDataFetcher(test_points)
    texture_mapped_values = soil_fetcher.get_soil_texture_values()
    print(texture_mapped_values)
