import pytest
from pathlib import Path
import pandas as pd
import geopandas as gpd
from datetime import datetime
from shapely.geometry import Point
from src.data_loader.get_farm_data import FarmDataManager  

@pytest.fixture
def farm_manager():
    input_file = "data/test/litefarm_test.csv"
    farm_id = "0369f026-1f90-11ee-b788-0242ac150004"
    crop = "Potato"
    return FarmDataManager(input_file=input_file, farm_id=farm_id, crop=crop)

# Test initialization
def test_initialization(farm_manager):
    assert farm_manager.farm_id == "0369f026-1f90-11ee-b788-0242ac150004"
    assert farm_manager.crop == "Potato"
    assert Path(farm_manager.input_file_path).exists()

# Test data retrieval and processing
def test_get_farm_data(farm_manager):
    farm_data = farm_manager.get_farm_data()
    assert isinstance(farm_data, dict)
    assert 'yield' in farm_data
    assert 'area' in farm_data
    assert 'latitude' in farm_data
    assert 'longitude' in farm_data

# Test geospatial data processing
def test_get_farm_gdf(farm_manager):
    farm_gdf = farm_manager.get_farm_gdf()
    assert isinstance(farm_gdf, gpd.GeoDataFrame)
    assert 'province' in farm_gdf.columns

# Test province retrieval
def test_get_province(farm_manager):
    province = farm_manager.get_province()
    assert isinstance(province, str)
    assert len(province) > 0

# Test crop group mapping
def test_get_crop_group(farm_manager):
    crop_group = farm_manager.get_crop_group()
    assert isinstance(crop_group, str)

# Test data validation checks
def test_validate_data(farm_manager):
    with pytest.raises(TypeError):
        farm_manager.farm_data['yield'] = 'not a number'
        farm_manager.validate_data()
    with pytest.raises(ValueError):
        farm_manager.farm_data['yield'] = -10
        farm_manager.validate_data()

# Test incorrect data types
@pytest.mark.parametrize("field, value", [
    ("yield", 'not a number'),
    ("area", None),
    ("start_year", '1985'),
    ("end_year", 1990.5)
])
def test_validate_data_incorrect_types(farm_manager, field, value):
    farm_manager.farm_data[field] = value  # Corrected assignment to use dictionary access
    with pytest.raises(TypeError):
        farm_manager.validate_data()

# Test zero and negative values for yield and area
@pytest.mark.parametrize("field, value", [
    ("yield", 0),
    ("area", -1)
])
def test_validate_data_zero_negative(farm_manager, field, value):
    farm_manager.farm_data[field] = value  # Corrected assignment to use dictionary access
    with pytest.raises(ValueError):
        farm_manager.validate_data()

# Test year out of valid range
@pytest.mark.parametrize("field, value", [
    ("start_year", 1983),
    ("end_year", datetime.now().year + 1)
])
def test_validate_data_invalid_year(farm_manager, field, value):
    farm_manager.farm_data[field] = value  # Corrected assignment to use dictionary access
    with pytest.raises(ValueError):
        farm_manager.validate_data()