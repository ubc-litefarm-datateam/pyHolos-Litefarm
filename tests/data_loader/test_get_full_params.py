import pytest
import numpy as np
from src.data_loader.get_full_params import FarmDataHub


@pytest.fixture
def farm_data_hub():
    test_input_file = "data/test/hypothetical_farm_data.csv"
    test_farm_id = "farm1"
    test_crop = "Potato"
    return FarmDataHub(
        input_file=test_input_file,
        farm_id=test_farm_id,
        crop=test_crop,
        source="external",
        operation_mode="scientific",
        num_runs=10,
    )


def test_scientific_mode_lengths(farm_data_hub):
    scientific_params = farm_data_hub.gather_all_data()
    # Check lengths of arrays for farm data and scientific data
    assert (
        len(scientific_params["farm_data"]["farm_id"]) == 1
    ), "Farm data should have exactly one element"

    # Ensure that all scientific data arrays have num_runs + 1 elements
    for param, value in scientific_params.items():
        if param != "farm_data":
            for sub_param, sub_value in value.items():
                assert (
                    len(sub_value) == farm_data_hub.num_runs + 1
                ), f"Length of {sub_param} should be {farm_data_hub.num_runs + 1}"


def test_values_match_external_farmer_mode(farm_data_hub):
    # Setup for farmer's mode with external data
    farm_params_external = FarmDataHub(
        input_file=farm_data_hub.input_file,
        farm_id=farm_data_hub.farm_id,
        crop=farm_data_hub.crop,
        source="external",
        operation_mode="farmer",
    )
    farmer_external_params = farm_params_external.gather_all_data()

    # Setup for scientific mode
    scientific_params = farm_data_hub.gather_all_data()

    # Compare the first values of scientific mode with external farmer mode
    for param_group, group_dict in scientific_params.items():
        if param_group != "farm_data":  # Assuming farm_data does not require this check
            for param, values in group_dict.items():
                assert np.isclose(
                    values[0], farmer_external_params[param_group][param][0], rtol=1e-5
                ).all(), f"First value of {param} in scientific mode does not match farmer's mode"


@pytest.fixture
def farm_data_hub_default():
    test_input_file = "data/test/hypothetical_farm_data.csv"
    test_farm_id = "farm1"
    test_crop = "Potato"
    return FarmDataHub(
        input_file=test_input_file,
        farm_id=test_farm_id,
        crop=test_crop,
        source="default",
        operation_mode="farmer",
    )


def test_default_mode_data_integrity(farm_data_hub_default):
    default_params = farm_data_hub_default.gather_all_data()
    
    expected_farm_data = np.array(
        ["farm1"], dtype="<U36"
    )
    assert np.array_equal(
        default_params["farm_data"]["farm_id"], expected_farm_data
    ), "Farm ID does not match expected default data"
