import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.data_loader.get_default_soil_texture import ModifierSoilTexture

def test_get_region_western():
    farm_data = {'province': 'Alberta'}
    modifier = ModifierSoilTexture(farm_data)
    assert modifier.get_region() == 'western_canada'

def test_get_region_eastern():
    farm_data = {'province': 'Quebec'}
    modifier = ModifierSoilTexture(farm_data)
    assert modifier.get_region() == 'eastern_canada'

def test_get_rf_tx_modifier():
    farm_data = {'province': 'Quebec'}
    soil_texture = 'fine'
    modifier = ModifierSoilTexture(farm_data, soil_texture)
    rf_tx = modifier.get_rf_tx_modifier()
    assert rf_tx == 2.55
    
