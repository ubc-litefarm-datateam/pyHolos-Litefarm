from unittest.mock import patch
import pytest
import numpy as np
from src.data_loader.get_modifiers import ModifiersManager


@pytest.fixture
def farm_data():
    """Provides a dictionary with test farm data."""
    return {"province": "Alberta"}


@pytest.fixture
def mod_manager(farm_data):
    """Provides an instance of ModifiersManager with test farm data."""
    return ModifiersManager(farm_data)


def test_calculated_modifiers(mod_manager):
    """
    Test to ensure that the calculated modifiers match the expected values
    for given farm data.
    """
    expected_modifiers = {
        "RF_AM": np.array([1.0]),
        "RF_CS": np.array([1.0]),
        "RF_NS": np.array([0.84]),
        "RF_Till": np.array([1.0]),
    }
    assert (
        mod_manager.modifiers == expected_modifiers
    ), "Calculated modifiers do not match the expected values."


def test_sample_modifiers_length(mod_manager):
    """
    Test to ensure the number of samples in the returned dictionary matches
    the specified num_samples.
    """
    num_samples = 10
    sampled_modifiers = mod_manager.sample_modifiers(num_samples=num_samples)
    for key, values in sampled_modifiers.items():
        assert (
            len(values) == num_samples + 1
        ), f"Number of samples for {key} is incorrect."


def test_user_defined_sampling_error(mod_manager):
    """
    Test to ensure that trying to sample with user-defined distributions without proper
    distributions raises a ValueError.
    """
    # Mock 'load_user_distributions' to return None or an empty dictionary as needed
    with patch.object(ModifiersManager, 'load_user_distributions', return_value=None):
        with pytest.raises(ValueError, match="No user-defined RF distributions found"):
            mod_manager.sample_modifiers(sampling_mode="user_define")
