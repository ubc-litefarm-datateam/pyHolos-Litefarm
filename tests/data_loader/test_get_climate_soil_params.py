import pytest
from src.data_loader.get_farm_data import FarmDataManager
from src.data_loader.get_climate_soil_params import ClimateSoilDataManager


# Fixtures to setup data for tests
@pytest.fixture(scope="module")
def farm_data():
    input_file = "data/test/hypothetical_farm_data.csv"
    farm_id = "farm1"
    crop = "Soybean"
    return FarmDataManager(input_file=input_file, farm_id=farm_id, crop=crop)


@pytest.fixture(scope="module")
def manager_default(farm_data):
    return ClimateSoilDataManager(farm_data, source="default")


@pytest.fixture(scope="module")
def manager_external_farmer(farm_data):
    return ClimateSoilDataManager(farm_data, source="external")


@pytest.fixture(scope="module")
def manager_external_scientific(farm_data):
    return ClimateSoilDataManager(
        farm_data, source="external", operation_mode="scientific", num_runs=10
    )


def test_eco_id_added(manager_default, farm_data):
    manager_default.get_climate_soil_data()
    assert "eco_id" in farm_data.farm_data, "eco_id should be added to the farm data"
    assert manager_default.eco_id is not None, "eco_id should not be none."
    assert manager_default.eco_id == 950, "eco_id is incorrect"


def test_farmer_mode_outputs(manager_default, manager_external_farmer):
    result_default = manager_default.get_climate_soil_data()
    result_external = manager_external_farmer.get_climate_soil_data()

    assert round(result_default["P"][0], 2) == 512.0
    assert round(result_default["PE"][0], 2) == 483.0
    assert round(result_default["soil_texture"][0], 2) == 1.0

    assert round(result_external["P"][0], 2) == 433.46
    assert round(result_external["PE"][0], 2) == 407.51
    assert round(result_external["soil_texture"][0], 2) == 0.8


def test_scientific_mode_lengths(manager_external_scientific):
    result_scientific = manager_external_scientific.get_climate_soil_data()

    assert len(result_scientific["P"]) == 11  # 10 random points + 1 farm point
    assert result_scientific["P"][0] == 433.46
    assert result_scientific["PE"][0] == 407.51
    assert result_scientific["FR_Topo"][0] == 0
    assert result_scientific["locations"][0][0] == -123.2373389
    assert result_scientific["locations"][0][1] == 49.99704167
    assert result_scientific["soil_texture"][0] == 0.8
