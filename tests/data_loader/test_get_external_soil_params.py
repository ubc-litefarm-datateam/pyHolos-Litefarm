import pytest
import numpy as np
from src.data_loader.get_external_soil_params import ExternalSoilTextureDataFetcher


def test_get_soil_texture_integration():
    """
    Test the ExternalSoilTextureDataFetcher with real data to ensure it correctly
    maps soil texture data to geographical points based on actual data files.
    """
    # Test input points
    test_points = [
        (-93.6250, 42.0329),
        (-89.3985, 43.0731),
        (-122.9618, 49.2957),
    ]

    # Expected output
    expected_output = {
        (-93.6250, 42.0329): 1.09,
        (-89.3985, 43.0731): np.nan,
        (-122.9618, 49.2957): np.nan,
    }

    # Initialize the data fetcher
    soil_fetcher = ExternalSoilTextureDataFetcher(test_points)

    # Fetch the soil textures
    result = soil_fetcher.get_soil_texture_values()

    # Assert the results are as expected, handle floating points and NaNs
    assert (
        result == expected_output
    ), "The fetched soil texture values do not match the expected output."

