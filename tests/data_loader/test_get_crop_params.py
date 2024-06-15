from unittest.mock import patch
import pytest
import numpy as np
from src.data_loader.get_crop_params import CropParametersManager


@pytest.fixture
def test_farm_data():
    return {"crop": "Oats"}


@pytest.fixture
def test_climate_data():
    return {"P": np.array([100]), "PE": np.array([120])}


@pytest.fixture
def crop_parameters_manager(test_farm_data, test_climate_data):
    return CropParametersManager(test_farm_data, test_climate_data)


def test_crop_parameters(crop_parameters_manager):
    expected_parameters = {
        "moisture": np.array([12.0]),
        "R_p": np.array([0.319]),
        "R_s": np.array([0.283]),
        "R_r": np.array([0.241]),
        "R_e": np.array([0.157]),
        "N_p": np.array([18.0]),
        "N_s": np.array([6.0]),
        "N_r": np.array([10.0]),
        "N_e": np.array([10.0]),
    }
    assert (
        crop_parameters_manager.crop_parameters == expected_parameters
    ), "Crop parameters do not match expected values"


def test_default_sampled_parameters_length(crop_parameters_manager):
    num_samples = 10
    sampled_params = crop_parameters_manager.sample_crop_parameters(
        num_samples=num_samples
    )
    for key, value in sampled_params.items():
        assert len(value) == num_samples + 1, f"Incorrect number of samples for {key}"


def test_user_defined_sampling_error(crop_parameters_manager):
    """
    Test to ensure that trying to sample with 'user_define' mode raises a ValueError
    when no user-defined distributions are found.
    """
    with patch.object(
        CropParametersManager, "load_user_distributions", return_value=None
    ):
        with pytest.raises(ValueError, match="No user-defined distributions found"):
            crop_parameters_manager.sample_crop_parameters(sampling_mode="user_define")

    with patch.object(
        CropParametersManager, "load_user_distributions", return_value={}
    ):
        with pytest.raises(ValueError, match="No user-defined distributions found"):
            crop_parameters_manager.sample_crop_parameters(sampling_mode="user_define")


def test_user_defined_sampling_success(crop_parameters_manager):
    """
    Test successful sampling using user-defined distributions.
    """
    mock_distributions = {
        "Oats": {
            "moisture": ["uniform", 10, 15]
        }
    }
    with patch.object(
        CropParametersManager,
        "load_user_distributions",
        return_value=mock_distributions,
    ):
        sampled_params = crop_parameters_manager.sample_crop_parameters(
            sampling_mode="user_define", num_samples=10
        )
        assert "moisture" in sampled_params, "Moisture should be sampled"
        assert (
            len(sampled_params["moisture"]) == 11
        ), "Should return 11 samples for moisture"
