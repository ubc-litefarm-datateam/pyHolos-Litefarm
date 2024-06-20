from unittest.mock import patch
import pytest
import numpy as np
from src.data_loader.get_crop_group_params import (
    CropGroupManager,
) 


# Fixtures for consistent test setup
@pytest.fixture
def test_farm_data():
    return {"crop": "Wheat"}


@pytest.fixture
def crop_group_manager(test_farm_data):
    return CropGroupManager(test_farm_data)


# Test to check if the parameters are retrieved correctly
def test_crop_group_parameters(crop_group_manager):
    expected_params = {
        "carbon_concentration": np.array([0.45]),
        "S_s": np.array([100.0]),
        "S_r": np.array([100.0]),
        "S_p": np.array([2.0]),
    }
    assert (
        crop_group_manager.crop_group_params == expected_params
    ), "Crop group parameters do not match expected values"


# Test to check if the default sampled parameters array length is correct
def test_default_sampled_parameters_length(crop_group_manager):
    num_samples = 10
    sampled_params = crop_group_manager.sample_crop_group_parameters(
        num_samples=num_samples
    )
    for key, value in sampled_params.items():
        assert (
            len(value) == num_samples + 1
        ), f"Length of sampled data for {key} is incorrect"


# Test to check error raising when user-defined distributions are not found
def test_user_defined_sampling_error(crop_group_manager):
    """
    Test to ensure that trying to sample with 'user_define' mode raises a ValueError
    when no user-defined distributions are found.
    """
    # Mock load_user_distributions to return None
    with patch.object(CropGroupManager, "load_user_distributions", return_value=None):
        with pytest.raises(
            ValueError, match="No user-defined distributions found for the crop group"
        ):
            crop_group_manager.sample_crop_group_parameters(sampling_mode="user_define")

    # Alternatively, mock to return an empty dictionary
    with patch.object(CropGroupManager, "load_user_distributions", return_value={}):
        with pytest.raises(
            ValueError, match="No user-defined distributions found for the crop group"
        ):
            crop_group_manager.sample_crop_group_parameters(sampling_mode="user_define")


# Test to ensure KeyError is raised if parameter not found
def test_key_error_for_missing_parameter(crop_group_manager):
    """
    Test to ensure that trying to sample with 'user_define' mode raises a KeyError
    when a required parameter is not found in the user-defined distributions.
    """
    # Mock load_user_distributions to return a dictionary missing the required parameter
    mocked_distributions = {
        "Annual": {
            "some_parameter": [
            "uniform",
            0.4,
            0.5
        ],
        } 
    }
    with patch.object(
        CropGroupManager, "load_user_distributions", return_value=mocked_distributions
    ):
        with pytest.raises(KeyError):
            crop_group_manager.sample_crop_group_parameters(sampling_mode="user_define")
