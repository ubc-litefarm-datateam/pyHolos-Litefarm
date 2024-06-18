import sys
import os
import json
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data_loader.get_farm_data import FarmDataManager
from data_loader.get_climate_soil_params import ClimateSoilDataManager
from data_loader.get_modifiers import ModifiersManager
from data_loader.get_crop_group_params import CropGroupManager
from data_loader.get_crop_params import CropParametersManager


class FarmDataHub:
    """
    Manages the aggregation of various farm-related data including climate data, 
    modifiers, crop parameters, and crop group parameters. This class acts as 
    a coordinator for fetching and integrating data from multiple data sources 
    based on the specified farm setup and operational modes.

    Attributes
    ----------
    input_file : str
        Path to the file containing the farm's data.
    farm_id : str
        Unique identifier for the farm.
    crop : str
        The type of crop grown on the farm.
    source : str
        The source of the data ('default' or 'external').
    operation_mode : str
        The mode of operation, affecting how data is retrieved and processed 
        ('farmer' or 'scientific').
    num_runs : int
        Number of runs or samples to generate in 'scientific' mode.
    sampl_modifier : str
        Sampling mode for modifiers ('default' or 'user_define').
    sampl_crop : str
        Sampling mode for crop parameters ('default' or 'user_define').
    sampl_crop_group : str
        Sampling mode for crop group parameters ('default' or 'user_define').

    Methods
    -------
    gather_all_data()
        Coordinates the retrieval of farm data, climate and soil parameters, modifiers (
        i.e., reduction factors), crop-related parameters, and crop group-related parameters
        based on the specified data source and operation mode. This method acts as the central 
        function called to initiate data fetching and integration.

    Raises
    ------
    ValueError
        If an invalid parameter length is detected during data assembly or if an invalid 
        combination of source and operation mode is provided.
    """
    def __init__(
        self,
        input_file,
        farm_id,
        crop,
        source="default",
        operation_mode="farmer",
        num_runs=10,
        sampl_modifier="default",
        sampl_crop="default",
        sampl_crop_group="default",
    ):
        self.input_file = input_file
        self.farm_id = farm_id
        self.crop = crop
        self.source = source
        self.operation_mode = operation_mode
        self.num_runs = num_runs
        self.sampl_modifier = sampl_modifier
        self.sampl_crop = sampl_crop
        self.sampl_crop_group = sampl_crop_group

    def gather_all_data(self):
        """
        Gathers all necessary data from various managers, handles different data sources 
        and operational modes, and returns a comprehensive dictionary of all farm data.

        Returns
        -------
        dict
            A dictionary containing structured data for farm, climate, crop parameters, 
            crop group parameters, and modifiers, formatted for further analysis or display.

        Raises
        ------
        ValueError
            If an invalid parameter length is detected in the assembled data or if an invalid 
            source and operation mode combination is provided.
        """
        farm = FarmDataManager(
            input_file=self.input_file, farm_id=self.farm_id, crop=self.crop
        )
        farm_data = farm.farm_data

        if self.source == "default":
            climate_data_extractor = ClimateSoilDataManager(
                farm,
                source=self.source,
            )
            climate_data = climate_data_extractor.get_climate_soil_data()
            eco_id = climate_data_extractor.eco_id
            farm_data["eco_id"] = eco_id
            modifiers_manager = ModifiersManager(farm_data)
            modifiers = modifiers_manager.modifiers
            crop_parameters_manager = CropParametersManager(farm_data, climate_data)
            crop_params = crop_parameters_manager.crop_parameters
            crop_group_manager = CropGroupManager(farm_data)
            crop_group_params = crop_group_manager.crop_group_params

            all_params = {
                "farm_data": {k: np.array([v]) for k, v in farm_data.items()},
                # 'farm_data': farm_data,
                "crop_group_params": crop_group_params,
                "crop_parameters": crop_params,
                "climate_data": climate_data,
                "modifiers": modifiers,
            }

            for params_group, group_dict in all_params.items():
                for param, value in group_dict.items():
                    if len(value) == 1:
                        pass
                    else:
                        raise ValueError(
                            f"Invalid parameter length for {param}. Halted."
                        )

            return all_params

        if self.source == "external" and self.operation_mode == "farmer":
            climate_data_extractor = ClimateSoilDataManager(
                farm, source=self.source, operation_mode=self.operation_mode
            )
            climate_data = climate_data_extractor.get_climate_soil_data()
            eco_id = climate_data_extractor.eco_id
            farm_data["eco_id"] = eco_id
            modifiers_manager = ModifiersManager(farm_data)
            modifiers = modifiers_manager.modifiers
            crop_parameters_manager = CropParametersManager(farm_data, climate_data)
            crop_params = crop_parameters_manager.crop_parameters
            crop_group_manager = CropGroupManager(farm_data)
            crop_group_params = crop_group_manager.crop_group_params

            all_params = {
                "farm_data": {k: np.array([v]) for k, v in farm_data.items()},
                "crop_group_params": crop_group_params,
                "crop_parameters": crop_params,
                "climate_data": climate_data,
                "modifiers": modifiers,
            }

            for params_group, group_dict in all_params.items():
                for param, value in group_dict.items():
                    if len(value) == 1:
                        pass
                    else:
                        raise ValueError(
                            f"Invalid parameter length for {param}. Halted."
                        )

            return all_params

        if self.source == "external" and self.operation_mode == "scientific":
            climate_data_extractor = ClimateSoilDataManager(
                farm,
                source=self.source,
                operation_mode=self.operation_mode,
                num_runs=self.num_runs,
            )
            climate_data = climate_data_extractor.get_climate_soil_data()

            eco_id = climate_data_extractor.eco_id
            farm_data["eco_id"] = eco_id

            modifiers_manager = ModifiersManager(farm_data)
            modifiers = modifiers_manager.sample_modifiers(
                sampling_mode=self.sampl_modifier, num_samples=self.num_runs
            )

            crop_parameters_manager = CropParametersManager(farm_data, climate_data)
            crop_params = crop_parameters_manager.sample_crop_parameters(
                sampling_mode=self.sampl_crop, num_samples=self.num_runs
            )

            crop_group_manager = CropGroupManager(farm_data)
            crop_group_params = crop_group_manager.sample_crop_group_parameters(
                sampling_mode=self.sampl_crop_group, num_samples=self.num_runs
            )

            all_params = {
                "farm_data": {k: np.array([v]) for k, v in farm_data.items()},
                "crop_group_params": crop_group_params,
                "crop_parameters": crop_params,
                "climate_data": climate_data,
                "modifiers": modifiers,
            }

            for params_group, group_dict in all_params.items():
                if params_group == "farm_data":
                    for param, value in group_dict.items():
                        if len(value) == 1:
                            pass
                        else:
                            raise ValueError(
                                f"Invalid parameter length for {param}. Halted."
                            )
                else:
                    for param, value in group_dict.items():
                        if len(value) == self.num_runs + 1:
                            pass
                        else:
                            raise ValueError(
                                f"Invalid parameter length for {param}. Halted."
                            )

            return all_params

        raise ValueError("Scientific mode cannot be run. Excution Halted.")


# Example usage
if __name__ == "__main__":
    test_input_file = "data/test/litefarm_test.csv"
    test_farm_id = "0369f026-1f90-11ee-b788-0242ac150004"
    test_crop = "Potato"
    farm_params = FarmDataHub(
        input_file=test_input_file,
        farm_id=test_farm_id,
        crop=test_crop,
        source="default",
        operation_mode="farmer",
    )
    farmer_holos_default_params = farm_params.gather_all_data()
    print("Farmer's mode with Holos default data:", farmer_holos_default_params)

    farm_params2 = FarmDataHub(
        input_file=test_input_file,
        farm_id=test_farm_id,
        crop=test_crop,
        source="external",
        operation_mode="farmer",
    )
    farmer_external_params = farm_params2.gather_all_data()
    print("Farmer's mode with external climate & soil data:", farmer_external_params)

    farm_params3 = FarmDataHub(
        input_file=test_input_file,
        farm_id=test_farm_id,
        crop=test_crop,
        source="external",
        operation_mode="scientific",
    )
    scientific_params = farm_params3.gather_all_data()
    print("Scientific mode:", scientific_params)

    files = {
        "farmer_holos_default_params": farmer_holos_default_params,
        "farmer_external_params": farmer_external_params,
        "scientific_params": scientific_params,
    }

    class NumpyEncoder(json.JSONEncoder):
        """Custom encoder for numpy data types"""

        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return json.JSONEncoder.default(self, obj)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    for key, params in files.items():
        output_file = f"{key}.json"  # This will create filenames based on the keys
        output_path = os.path.join(dir_path, "..", "..", "data", "temp", output_file)

        # Write the JSON data to the file
        with open(output_path, "w") as f:
            json.dump(params, f, indent=4, cls=NumpyEncoder)

        print(f"Saved {key} to {output_path}")
