import pytest
import numpy as np
from src.emission_factor_aggregator import EmissionFactorAggregator

@pytest.fixture
def data_farmer():
    return {
        'farm_data': {'area': np.array([0.1409]), 
                      'latitude': np.array([46.4761852]), 
                      'longitude': np.array([-71.5189528]), 
                      'crop': np.array(['Soybean'], dtype='<U7'), 
                      'yield': np.array([2700.]), 
                      'start_year': np.array([2021]), 
                      'end_year': np.array([2021]), 
                      'province': np.array(['Quebec'], dtype='<U6')}, 
        'climate_data': {'P': np.array([652.]), 
                         'PE': np.array([556.]), 
                         'FR_Topo': np.array([11.71]), 
                         'locations': np.array([[-71.5189528,  46.4761852]]), 
                         'soil_texture': np.array([0.49])}, 
        'modifiers': {'RF_AM': np.array([1.]), 
                      'RF_CS': np.array([1.]), 
                      'RF_NS': np.array([0.84]), 
                      'RF_Till': np.array([1.])}
    }

@pytest.fixture
def data_scientific():
    return {
        'farm_data': {'area': np.array([0.1409,0.2409,0.3409]), 
                      'latitude': np.array([46.4761852,46.4761852,46.4761852]), 
                      'longitude': np.array([-71.5189528,-71.5189528,-71.5189528]), 
                      'crop': np.array(['Soybean','Soybean','Soybean'], dtype='<U7'), 
                      'yield': np.array([2700, 3700, 4700]), 
                      'start_year': np.array([2021,2021,2021]), 
                      'end_year': np.array([2021,2021,2021]), 
                      'province': np.array(['Quebec','Quebec','Quebec'], dtype='<U6')}, 
        'climate_data': {'P': np.array([652,752,852]), 
                         'PE': np.array([556,656,756]), 
                         'FR_Topo': np.array([11.71,22.71,33.71]), 
                         'locations': np.array([[-71.5189528,  46.4761852],[-71.5189528,  46.4761852],[-71.5189528,  46.4761852]]), 
                         'soil_texture': np.array([0.49,0.59,0.69])}, 
        'modifiers': {'RF_AM': np.array([1,1,1]), 
                      'RF_CS': np.array([1,1,1]), 
                      'RF_NS': np.array([0.84,0.84,0.84]), 
                      'RF_Till': np.array([1,1,1])}
    }

def test_farmer_mode_output(data_farmer):
    aggregator = EmissionFactorAggregator(data_farmer)
    output = aggregator.get_result()
    assert isinstance(output, dict)
    assert 'EF_CT_P' in output
    assert len(output['EF_CT_P']) == 1

def test_scientific_mode_output(data_scientific):
    aggregator = EmissionFactorAggregator(data_scientific, operation_mode='scientific')
    output = aggregator.get_result()
    assert isinstance(output, dict)
    assert 'P' in output
    assert len(output['P']['EF_CT_P']) == 3

def test_data_preparation(data_farmer):
    aggregator = EmissionFactorAggregator(data_farmer)
    prepared_data = aggregator.prepare_data_for_efc('P', 700)
    assert prepared_data['climate_data']['P'] == 700

def test_error_handling_missing_data(data_farmer):
    incomplete_data = data_farmer.copy()
    del incomplete_data['climate_data']['P']
    with pytest.raises(ValueError):
        aggregator = EmissionFactorAggregator(incomplete_data)
        aggregator.get_result()
