import os
import sys
import numpy as np
import pandas as pd
import geopandas as gpd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.data_loader.get_external_climate_params import ExternalClimateDataFetcher
from src.data_loader.get_external_soil_params import ExternalSoilTextureDataFetcher
from src.data_loader.generate_random_points import generate_random_points, extract_lon_lat
from src.data_loader.get_default_soil_texture import ModifierSoilTexture
from src.data_loader.sampling_fr_topo import sampling_fr_topo


class ClimateSoilDataManager:
    """
    Manages the integration and processing of climate and soil data for specific farm locations.

    This class handles the retrieval, integration, and preprocessing of climate and soil data,
    either from default data sources or external data services, tailored to the needs of either
    farmer-specific or scientific research purposes.

    Attributes
    ----------
    farm_data : FarmData
        An instance of the FarmData class containing information about the farm.
    source : str
        The source of the data ('default' or 'external').
    operation_mode : str
        The mode of operation which determines how data is retrieved and processed
        ('farmer' or 'scientific').
    num_runs : int
        The number of data retrieval runs, applicable in 'scientific' mode.
    farm_point : tuple
        A tuple containing the longitude and latitude of the farm.
    year_range : tuple
        A tuple containing two integers, representing the start and end years for which climate
        data should be fetched.
    dir : str
        The directory path to the module's location.
    climate_soil_dict : dict or None
        A dictionary holding the climate and soil data after processing.
    eco_id : str or None
        The ecodistrict ID associated with the farm.

    Methods
    -------
    load_default_climate_soil_data()
        Loads Holos climate and soil data for ecodistricts from a CSV file.
    load_ecodistrict_polygons()
        Loads the ecodistrict polygons from a shapefile.
    extract_farm_ecoid_df()
        Extracts the ecodistrict ID for the farm.
    extract_farm_ecodistrict_polygon()
        Retrieves the polygon geometry of the farm's ecodistrict.
    extract_default_climate_soil_data()
        Extracts and processes default climate and soil data for the farm based on
        the farm's ecodistrict ID.
    get_climate_soil_data()
        Retrieves climate and soil data based on the source and operation mode specified.
    """

    def __init__(
        self, farm_data, source="default", operation_mode="farmer", num_runs=10
    ):
        self.farm_data = farm_data
        self.source = source
        self.operation_mode = operation_mode
        self.num_runs = num_runs
        self.farm_point = (
            self.farm_data.farm_data["longitude"],
            self.farm_data.farm_data["latitude"],
        )
        self.year_range = (
            self.farm_data.farm_data["start_year"],
            self.farm_data.farm_data["end_year"],
        )
        self.dir = os.path.dirname(__file__)
        self.climate_soil_dict = None  # Initialize the climate data dictionary as None
        self.eco_id = None

    def load_default_climate_soil_data(self):
        """
        Loads default Holos climate and soil data for ecodistricts from a CSV file.

        Returns
        -------
        DataFrame
            A pandas DataFrame containing climate and soil related information.
        """
        climate_path = os.path.join(
            self.dir, "../../data/raw/Holos/ecodistrict_to_ecozone_mapping.csv"
        )
        return pd.read_csv(climate_path)

    def load_ecodistrict_polygons(self):
        """
        Loads and returns the ecodistrict polygons from a shapefile.

        Returns
        -------
        GeoDataFrame
            A geopandas GeoDataFrame containing ecodistrict polygons.
        """
        ecodistrict_path = os.path.join(
            self.dir, "../../data/external/slc_dissolved_ecodistrict"
        )
        ecodistrict = gpd.read_file(ecodistrict_path)
        return ecodistrict.to_crs("EPSG:4326")

    def extract_farm_ecoid_df(self):
        """
        Extracts the farm's ecodistrict ID and merges it with the farm's geospatial data.

        Returns
        -------
        DataFrame
            A pandas DataFrame with the farm's data including the ecodistrict ID.
        """
        ecodistrict = self.load_ecodistrict_polygons()
        farm_ecoid_df = gpd.sjoin(
            self.farm_data.farm_gdf,
            ecodistrict[["ECO_ID", "geometry"]],
            how="left",
            predicate="within",
        ).drop(columns=["index_right"])
        return farm_ecoid_df

    def extract_farm_ecodistrict_polygon(self):
        """
        Retrieves the polygon geometry of the ecodistrict that contains the farm.

        Returns
        -------
        geometry
            The polygon geometry of the farm's ecodistrict.
        """
        ecodistrict = self.load_ecodistrict_polygons()
        farm_ecodistrict = gpd.sjoin(
            ecodistrict, self.farm_data.farm_gdf, how="inner", predicate="contains"
        )
        return farm_ecodistrict["geometry"].iloc[0]

    def extract_default_climate_soil_data(self):
        """
        Extracts and processes default climate and soil data for the farm based on
        the farm's ecodistrict ID.

        This method assumes that data merging will be successful and relevant columns
        are available. Populates the `climate_soil_dict` attribute with default climate
        and soil data.
        """
        farm_ecoid_df = self.extract_farm_ecoid_df()
        default_climate_df = self.load_default_climate_soil_data()

        farm_ecoid_climate_soil = pd.merge(
            farm_ecoid_df,
            default_climate_df,
            how="left",
            left_on=["ECO_ID", "province"],
            right_on=["Ecodistrict", "Province"],
        ).drop(columns=["ECO_ID", "Ecozone", "province", "SoilType"])

        self.climate_soil_dict = {
            # "soil_texture": np.array([farm_ecoid_climate_soil["SoilTexture"].iloc[0].lower()]),
            "P": np.array([float(farm_ecoid_climate_soil["PMayToOct"].iloc[0])]),
            "PE": np.array([float(farm_ecoid_climate_soil["PEMayToOct"].iloc[0])]),
            "FR_Topo": np.array([float(farm_ecoid_climate_soil["Ftopo"].iloc[0])]),
            "locations": np.array([self.farm_point]),
        }

        # Handling soil texture and modifying it if necessary
        soil_texture_type = farm_ecoid_climate_soil["SoilTexture"].iloc[0].lower()
        rf_tx_fetcher = ModifierSoilTexture(self.farm_data.farm_data, soil_texture_type)
        rf_tx_value = rf_tx_fetcher.get_rf_tx_modifier()
        self.climate_soil_dict["soil_texture"] = np.array([rf_tx_value])

        # Storing the Ecodistrict ID
        self.eco_id = farm_ecoid_climate_soil["Ecodistrict"].iloc[0]

    def fetch_external_data(self, points, years_range):
        """Fetch external climate and soil data for given points over specified years."""
        climate_fetcher = ExternalClimateDataFetcher(points, *years_range)
        soil_fetcher = ExternalSoilTextureDataFetcher(points)

        climate_data = climate_fetcher.process_points_over_years()
        soil_data = soil_fetcher.get_soil_texture_values()

        return climate_data, soil_data

    def process_data_points(self, points_list, climate_data, soil_data):
        """Process climate and soil data for a list of points."""
        results = {
            "locations": [],
            "P": [],
            "PE": [],
            "soil_texture": [],
        }

        for point in points_list:
            results["locations"].append(point)

            if climate_data[point]["success"]:
                results["P"].append(climate_data[point]["P"])
                results["PE"].append(climate_data[point]["PE"])
            else:
                results["P"].append(np.nan)
                results["PE"].append(np.nan)
                print(
                    f"Error fetching climate data for point {point}: {climate_data[point]['error']}"
                )

            results["soil_texture"].append(soil_data[point])

        return {key: np.array(value) for key, value in results.items()}

    def get_climate_soil_data(self):
        """
        Retrieves and processes climate and soil data based on the specified source
        and operation mode.

        This method initializes with default climate and soil data, then based on the c
        onfiguration, it may fetch climate and soik data from external sources.
        In 'scientific' operation mode, additional random points within the farm's ecodistrict
        are processed to simulate a broader range of data.

        Returns
        -------
        dict
            A dictionary containing processed climate and soil data which includes parameters
            precipitation ('P'), potential evapotranspiration ('PE'), soil texture,
            topographical features ('FR_Topo'), and the geographical locations of the data points.
            The dictionary is prepared based on the operation mode:
            - For 'farmer' mode, the data is specific to the farm's location.
                - For 'default' source, the data is retrieved from Holos default values for the
                  corresponding ecodistrict the farm is located in.
                - For 'external' source, the data is retrived from external sources specific farm's
                  location.
            - For 'scientific' mode, the data includes values from randomly generated points within
            the farm's ecodistrict as well as the farm's specific location (the first value of each
            numpy array).

        Raises
        ------
        ValueError
            If an invalid source or operation mode is specified, a ValueError is raised.

        Notes
        -----
        - The method assumes that the required paths to data files and configurations are
          correctly set in the class.
        - In 'scientific' mode, the FR Topo value for the farm point retains its default while
        values for randomly generated points are sampled using the `sampling_fr_topo` function.
        """
        if self.source == "default":
            self.extract_default_climate_soil_data()
            return self.climate_soil_dict

        if self.source == "external":
            self.extract_default_climate_soil_data()  # Initialize with default data
            points = [self.farm_point]

            if self.operation_mode == "scientific":
                polygon = self.extract_farm_ecodistrict_polygon()
                random_points = generate_random_points(
                    polygon, num_points=self.num_runs
                )
                points.extend(extract_lon_lat(random_points))

            climate_data, soil_data = self.fetch_external_data(points, self.year_range)
            processed_data = self.process_data_points(points, climate_data, soil_data)

            if self.operation_mode == "scientific":
                farm_ecod_fr_topo = self.climate_soil_dict["FR_Topo"][0]
                fr_topo_values = sampling_fr_topo(farm_ecod_fr_topo, self.num_runs)
                fr_topo_values = np.insert(fr_topo_values, 0, farm_ecod_fr_topo)
                self.climate_soil_dict["FR_Topo"] = fr_topo_values

            self.climate_soil_dict.update(processed_data)
            return self.climate_soil_dict

        print("Invalid source or operation mode.")
        return None


if __name__ == "__main__":
    from src.data_loader.get_farm_data import FarmDataManager

    test_input_file = "data/test/hypothetical_farm_data.csv"
    test_farm_id = "farm1"
    test_crop = "Soybean"
    test_farm_data = FarmDataManager(
        input_file=test_input_file, farm_id=test_farm_id, crop=test_crop
    )
    print(test_farm_data.farm_data)

    climate_soil_manager = ClimateSoilDataManager(
        test_farm_data, source="default"
    )  # operation_mode is default to 'farmer'
    climate_soil_data = climate_soil_manager.get_climate_soil_data()
    eco_id = climate_soil_manager.eco_id
    test_farm_data.farm_data["eco_id"] = eco_id
    print(test_farm_data.farm_data)
    print("Farmer's mode, get default P, PE, and soil texture ", climate_soil_data)

    climate_soil_manager2 = ClimateSoilDataManager(
        test_farm_data, source="external"
    )  # operation_mode is default to 'farmer'
    climate_soil_data2 = climate_soil_manager2.get_climate_soil_data()
    eco_id = climate_soil_manager2.eco_id
    test_farm_data.farm_data["eco_id"] = eco_id
    print(test_farm_data.farm_data)
    print("Farmer's mode, get external P, PE and soil texture: ", climate_soil_data2)

    climate_soil_manager3 = ClimateSoilDataManager(
        test_farm_data, source="external", operation_mode="scientific", num_runs=10
    )
    climate_soil_data3 = climate_soil_manager3.get_climate_soil_data()
    eco_id = climate_soil_manager3.eco_id
    test_farm_data.farm_data["eco_id"] = eco_id
    print(test_farm_data.farm_data)
    print(
        "Scientific mode, external P, PE and soil texture for 10 runs: ",
        climate_soil_data3,
    )
