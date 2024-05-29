import os
import json
import rasterio
import pandas as pd
import numpy as np

class ExternalSoilTextureDataFetcher:
    """
    A class to fetch and map soil texture data from external sources, 
    Harmonized World Soil Database v2.0, to specific geographical points.
    See details in
    https://www.fao.org/soils-portal/data-hub/soil-maps-and-databases/harmonized-world-soil-database-v20/en/.
    
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
        Open raster data source for reading raster data.

    Methods
    -------
    load_data()
        Loads necessary CSV data files into pandas dataframes.
    open_raster()
        Opens the raster file for reading geographical data.
    close_raster()
        Closes the open raster file.
    get_raster_value(lon, lat)
        Returns the soil mapping unit id from the raster at the specified coordinates.
    lookup_texture_and_value(smu_id)
        Looks up the texture type and mapped values using the specified SMU id.
    get_soil_texture()
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
            self.dir, '../../data/external/HWSD2/HWSD2_SMU.csv'
        )
        self.texture_csv_path = os.path.join(
            self.dir, '../../data/external/HWSD2/D_TEXTURE_USDA.csv'
        )
        self.raster_path = os.path.join(
            self.dir, '../../data/external/HWSD2_RASTER/HWSD2.bil'
        )
        self.texture_mapped_path = os.path.join(
            self.dir, '../../data/params_sampling_range/rf_tx_params_dist.json'
        )
        self.src = None
        self.load_data()
        
    def load_data(self):
        """Loads CSV data into pandas DataFrames from specified paths."""
        self.smu_df = pd.read_csv(self.smu_csv_path)
        self.texture_df = pd.read_csv(self.texture_csv_path)
        # self.mapped_value_df = pd.read_csv(self.texture_mapped_path)
    
    def load_user_rf_tx_distributions(self):
        with open(self.texture_mapped_path, 'r') as file:
            return json.load(file)
    
    def sampling_rf_tx(self, soil_type):
        rf_tx_distributions = self.load_user_rf_tx_distributions()
        if rf_tx_distributions is None:
            raise ValueError("No user-defined RF soil texture distributions found.")
        elif soil_type == "missing texture type" or soil_type == "no matching SMU ID":
            return np.nan
        else:
            low, high = rf_tx_distributions.get(soil_type)
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
            The SMU ID from the raster.
        """
        row, col = self.src.index(lon, lat)
        return self.src.read(1)[row, col]

    def lookup_texture_and_value(self, smu_id):
        """
        Looks up and returns the soil texture type and mapped value for 
        the texture based on the SMU_ID.
        
        Parameters
        ----------
        smu_id : int
            The soil mapping unit id (SMU_ID).

        Returns
        ----------
        float
            The mapped value corresponding to the texture type associated with the SMU id.
        """
        # Query the texture code from the SMU DataFrame
        query_result = self.smu_df[self.smu_df['HWSD2_SMU_ID'] == smu_id]['TEXTURE_USDA']
        if not query_result.empty:
            texture_code = query_result.iloc[0]            
            if not np.isnan(texture_code):
                texture_type = self.texture_df[self.texture_df['CODE'] == texture_code]['VALUE'].iloc[0]
                print(f"The soil texture type for SMU_ID {smu_id} is {texture_type}.")
                return texture_type
            else:
                print(f"No texture type found for SMU_ID {smu_id}; texture_type: 'missing texture type'.")
                return "missing texture type"
        else:
            print(f"No matching SMU_ID for the selected point; texture_type: 'no matching SMU ID'.")
            return "no matching SMU ID"

    def get_soil_texture(self):
        """
        Fetches soil texture values for all specified points and returns them.

        Returns
        ----------
        list of float
            Soil texture values for each specified point.
        """
        self.open_raster()
        rf_tx_values = {}
        for lon, lat in self.points:
            smu_id = self.get_raster_value(lon, lat)
            texture_type = self.lookup_texture_and_value(smu_id)
            rf_tx = self.sampling_rf_tx(texture_type)
            rf_tx_values[(lon, lat)] = rf_tx
        self.close_raster()

        return rf_tx_values

if __name__ == '__main__':
    # The first point has a match
    # The second point, texture_type is missing. this is because in the database, there is no
        # USDA_TEXTURE entry for this SMU 7001 (soil mapping unit). 
    # The third point is Vancouver Harbor, we don't have a valid SMU since it is water surface
        # HSWD2 has a high resolution 1km * 1km
    points = [(-93.6250, 42.0329), (-89.3985, 43.0731), (-122.9618, 49.2957)]  
    soil_fetcher = ExternalSoilTextureDataFetcher(points)
    texture_mapped_values = soil_fetcher.get_soil_texture()
    print(texture_mapped_values)
