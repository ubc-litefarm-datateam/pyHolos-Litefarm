import numpy as np
import pytest
from src.calculator.crop_residue_calculator import CropResidueCalculator
from src.calculator.crop_residue_aggregator import CropResidueAggregator

data_farm = {
    'farm_data': {
        'area': np.array([0.1409]),
        'latitude': np.array([46.4761852]),
        'longitude': np.array([-71.5189528]),
        'crop': np.array(['Soybean'], dtype='<U7'),
        'yield': np.array([2700.]),
        'start_year': np.array([2021]),
        'end_year': np.array([2021]),
        'province': np.array(['Quebec'], dtype='<U6'),
        'group': np.array(['annual'])
    },
    'crop_group_params': {
        'carbon_concentration': np.array([0.45]),
        'S_s': np.array([100.]),
        'S_r': np.array([100.]),
        'S_p': np.array([2.])
    },
    'crop_parameters': {
        'moisture': np.array([14.]),
        'R_p': np.array([0.304]),
        'R_s': np.array([0.455]),
        'R_r': np.array([0.146]),
        'R_e': np.array([0.095]),
        'N_p': np.array([67.]),
        'N_s': np.array([6.]),
        'N_r': np.array([10.]),
        'N_e': np.array([10.])
    },
    'climate_data': {
        'P': np.array([652.]),
        'PE': np.array([556.]),
        'FR_Topo': np.array([11.71]),
        'locations': np.array([[-71.5189528, 46.4761852]]),
        'soil_texture': np.array([0.49])
    },
    'modifiers': {
        'RF_AM': np.array([1.]),
        'RF_CS': np.array([1.]),
        'RF_NS': np.array([0.84]),
        'RF_Till': np.array([1.])
    }
}

data_sci = {
    'farm_data': {
        'area': np.array([0.1409]),
        'latitude': np.array([46.4761852]),
        'longitude': np.array([-71.5189528]),
        'crop': np.array(['Soybean'], dtype='<U7'),
        'yield': np.array([2700.]),
        'start_year': np.array([2021]),
        'end_year': np.array([2021]),
        'province': np.array(['Quebec'], dtype='<U6'),
        'group': np.array(['annual'])
    },
    'crop_group_params': {
        'carbon_concentration': np.array([0.45, 0.50, 0.55]),
        'S_s': np.array([100., 105., 110.]),
        'S_r': np.array([100., 105., 110.]),
        'S_p': np.array([2., 2.5, 3.])
    },
    'crop_parameters': {
        'moisture': np.array([14., 15., 16.]),
        'R_p': np.array([0.304, 0.314, 0.324]),
        'R_s': np.array([0.455, 0.465, 0.475]),
        'R_r': np.array([0.146, 0.156, 0.166]),
        'R_e': np.array([0.095, 0.105, 0.115]),
        'N_p': np.array([67., 70., 73.]),
        'N_s': np.array([6., 7., 8.]),
        'N_r': np.array([10., 11., 12.]),
        'N_e': np.array([10., 11., 12.])
    },
    'climate_data': {
        'P': np.array([652.]),
        'PE': np.array([556.]),
        'FR_Topo': np.array([11.71]),
        'locations': np.array([[-71.5189528, 46.4761852]]),
        'soil_texture': np.array([0.49])
    },
    'modifiers': {
        'RF_AM': np.array([1.]),
        'RF_CS': np.array([1.]),
        'RF_NS': np.array([0.84]),
        'RF_Till': np.array([1.])
    }
}

def test_initialization():
    aggregator = CropResidueAggregator(data_farm, 'farmer')
    assert aggregator.data == data_farm
    assert aggregator.mode == 'farmer'
    assert aggregator.target_data_group == ['crop_group_params', 'crop_parameters']
    assert isinstance(aggregator.calculator, CropResidueCalculator)

def test_get_baseline_data():
    aggregator = CropResidueAggregator(data_farm, 'farmer')
    baseline_data = aggregator.get_baseline_data()
    expected_baseline_data = {
        'farm_data': {
            'area': 0.1409,
            'yield': 2700.,
            'latitude': 46.4761852,
            'longitude': -71.5189528,
            'crop': 'Soybean',
            'start_year': 2021,
            'end_year': 2021,
            'province': 'Quebec',
            'group': 'annual'
        },
        'crop_group_params': {
            'carbon_concentration': 0.45,
            'S_s': 100.,
            'S_r': 100.,
            'S_p': 2.
        },
        'crop_parameters': {
            'moisture': 14.,
            'R_p': 0.304,
            'R_s': 0.455,
            'R_r': 0.146,
            'R_e': 0.095,
            'N_p': 67.,
            'N_s': 6.,
            'N_r': 10.,
            'N_e': 10.
        }
    }
    assert baseline_data == expected_baseline_data

def test_validate_mode_data_compatibility():
    aggregator = CropResidueAggregator(data_farm, 'farmer')
    with pytest.raises(ValueError):
        data_farm['crop_group_params']['carbon_concentration'] = np.array([0.45, 0.50])
        aggregator.validate_mode_data_compatibility()

def test_farmer_mode():
    data_farm_corrected = {
        'farm_data': {
            'area': np.array([0.1409]),
            'latitude': np.array([46.4761852]),
            'longitude': np.array([-71.5189528]),
            'crop': np.array(['Soybean'], dtype='<U7'),
            'yield': np.array([2700.]),
            'start_year': np.array([2021]),
            'end_year': np.array([2021]),
            'province': np.array(['Quebec'], dtype='<U6'),
            'group': np.array(['annual'])
        },
        'crop_group_params': {
            'carbon_concentration': np.array([0.45]),
            'S_s': np.array([100.]),
            'S_r': np.array([100.]),
            'S_p': np.array([2.])
        },
        'crop_parameters': {
            'moisture': np.array([14.]),
            'R_p': np.array([0.304]),
            'R_s': np.array([0.455]),
            'R_r': np.array([0.146]),
            'R_e': np.array([0.095]),
            'N_p': np.array([67.]),
            'N_s': np.array([6.]),
            'N_r': np.array([10.]),
            'N_e': np.array([10.])
        },
        'climate_data': {
            'P': np.array([652.]),
            'PE': np.array([556.]),
            'FR_Topo': np.array([11.71]),
            'locations': np.array([[-71.5189528, 46.4761852]]),
            'soil_texture': np.array([0.49])
        },
        'modifiers': {
            'RF_AM': np.array([1.]),
            'RF_CS': np.array([1.]),
            'RF_NS': np.array([0.84]),
            'RF_Till': np.array([1.])
        }
    }

    aggregator = CropResidueAggregator(data_farm_corrected, 'farmer')
    results = aggregator.farmer_mode()
    assert 'C_p' in results
    assert 'above_ground_carbon_input' in results
    assert 'below_ground_carbon_input' in results
    assert 'above_ground_residue_n' in results
    assert 'below_ground_residue_n' in results
    assert 'n_crop_residue' in results

def test_scientific_mode():
    aggregator = CropResidueAggregator(data_sci, 'scientific')
    results = aggregator.scientific_mode()
    for param in ['carbon_concentration', 'S_s', 'S_r', 'S_p']:
        assert param in results
        assert 'C_p' in results[param]
        assert 'above_ground_carbon_input' in results[param]
        assert 'below_ground_carbon_input' in results[param]
        assert 'above_ground_residue_n' in results[param]
        assert 'below_ground_residue_n' in results[param]
        assert 'n_crop_residue' in results[param]

def test_switch_to_farmer_mode():
    data_farm_corrected = {
        'farm_data': {
            'area': np.array([0.1409]),
            'latitude': np.array([46.4761852]),
            'longitude': np.array([-71.5189528]),
            'crop': np.array(['Soybean'], dtype='<U7'),
            'yield': np.array([2700.]),
            'start_year': np.array([2021]),
            'end_year': np.array([2021]),
            'province': np.array(['Quebec'], dtype='<U6'),
            'group': np.array(['annual'])
        },
        'crop_group_params': {
            'carbon_concentration': np.array([0.45]),
            'S_s': np.array([100.]),
            'S_r': np.array([100.]),
            'S_p': np.array([2.])
        },
        'crop_parameters': {
            'moisture': np.array([14.]),
            'R_p': np.array([0.304]),
            'R_s': np.array([0.455]),
            'R_r': np.array([0.146]),
            'R_e': np.array([0.095]),
            'N_p': np.array([67.]),
            'N_s': np.array([6.]),
            'N_r': np.array([10.]),
            'N_e': np.array([10.])
        },
        'climate_data': {
            'P': np.array([652.]),
            'PE': np.array([556.]),
            'FR_Topo': np.array([11.71]),
            'locations': np.array([[-71.5189528, 46.4761852]]),
            'soil_texture': np.array([0.49])
        },
        'modifiers': {
            'RF_AM': np.array([1.]),
            'RF_CS': np.array([1.]),
            'RF_NS': np.array([0.84]),
            'RF_Till': np.array([1.])
        }
    }

    aggregator = CropResidueAggregator(data_farm_corrected, 'scientific')
    assert aggregator.mode == 'farmer'

if __name__ == "__main__":
    pytest.main()
