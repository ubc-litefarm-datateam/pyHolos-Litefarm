import json
from unittest.mock import Mock
import pytest
from requests.exceptions import Timeout
from src.data_loader.get_external_climate_params import ExternalClimateDataFetcher

# Mock data for successful fetch
MOCK_SUCCESS_RESPONSE = {
    "header": {"start": "20210501", "end": "20210930"},
    "properties": {
        "parameter": {
            "PRECTOTCORR": {"20210501": 5, "20210502": 5},  # Simplified
            "T2M": {"20210501": 20, "20210502": 21},
            "RH2M": {"20210501": 50, "20210502": 55},
            "ALLSKY_SFC_SW_DWN": {"20210501": 200, "20210502": 210},
        }
    },
}


@pytest.fixture
def fetcher():
    return ExternalClimateDataFetcher([(-93.6250, 42.0329)], 2021, 2021)


def test_fetch_data_success(mocker, fetcher):
    # Mock the response from requests.get to return a successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = json.dumps(MOCK_SUCCESS_RESPONSE).encode(
        "utf-8"
    )  # Properly encode the JSON data
    mock_response.json.return_value = (
        MOCK_SUCCESS_RESPONSE  # Return JSON data when .json() is called
    )

    mocker.patch("requests.get", return_value=mock_response)

    result = fetcher.fetch_data((-93.6250, 42.0329), 2021)
    assert result["success"] is True
    assert "data" in result
    assert result["data"]["properties"]["parameter"]["PRECTOTCORR"]["20210501"] == 5


def test_fetch_data_failure(mocker, fetcher):
    # Simulate a timeout error
    mocker.patch("requests.get", side_effect=Timeout)
    result = fetcher.fetch_data((-93.6250, 42.0329), 2021)
    assert result["success"] is False
    assert "error" in result


def test_calculate_totals_with_incomplete_data(fetcher):
    # Simulate incomplete data
    incomplete_data = {
        "success": True,
        "data": MOCK_SUCCESS_RESPONSE,
        "point": (-93.6250, 42.0329),
        "year": 2021,
    }
    incomplete_data["data"]["properties"]["parameter"]["PRECTOTCORR"].pop("20210502")
    result = fetcher.calculate_totals(incomplete_data)
    assert result["success"] is False
    assert "error" in result
