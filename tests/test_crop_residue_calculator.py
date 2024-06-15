import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


import pytest
from src.crop_residue_calculator import CropResidueCalculator

@pytest.fixture
def test_data():
    return {
        "farm_data": {
            "area": 10,
            "yield": 5000,
            "group": "root"
        },
        "crop_group_params": {
            
            "carbon_concentration": 0.45,
            "S_p": 0,
            "S_s": 100,
            "S_r": 100
        },
        "crop_parameters": {
            "moisture": 80,
            "R_p": 0.626,
            "R_s": 0.357,
            "R_r": 0.01,
            "R_e": 0.007,
            "N_p": 10,
            "N_s": 29,
            "N_r": 10,
            "N_e": 10
        },
    }

@pytest.fixture
def setup(test_data):
    calculator = CropResidueCalculator(test_data)
    expected_c_p = (test_data["farm_data"]['yield'] + test_data["farm_data"]['yield'] * test_data["crop_group_params"]['S_p'] / 100) * (1 - test_data["crop_parameters"]['moisture'] / 100) * test_data["crop_group_params"]["carbon_concentration"]
    expected_c_p_to_soil = expected_c_p * test_data["crop_group_params"]['S_p'] / 100
    expected_c_s = expected_c_p * (test_data["crop_parameters"]['R_s'] / test_data["crop_parameters"]['R_p']) * (test_data["crop_group_params"]['S_s'] / 100)
    expected_c_r = expected_c_p * (test_data["crop_parameters"]['R_r'] / test_data["crop_parameters"]['R_p']) * (test_data["crop_group_params"]['S_r'] / 100)
    expected_c_e = expected_c_p * (test_data["crop_parameters"]['R_e'] / test_data["crop_parameters"]['R_p'])
    expected_grain_n = (expected_c_p_to_soil / 0.45) * (test_data["crop_parameters"]['N_p'] / 1000)
    expected_straw_n = (expected_c_s / 0.45) * (test_data["crop_parameters"]['N_s'] / 1000)
    expected_root_n = (expected_c_r / 0.45) * (test_data["crop_parameters"]['N_r'] / 1000)
    expected_exudate_n = (expected_c_e / 0.45) * (test_data["crop_parameters"]['N_e'] / 1000)
    expected_above_ground_residue_n = expected_straw_n
    expected_below_ground_residue_n = expected_grain_n + expected_exudate_n
    expected_n_crop_residue = (expected_above_ground_residue_n + expected_below_ground_residue_n) * test_data["farm_data"]['area']
    expected_above_ground_carbon_input = expected_c_s
    expected_below_ground_carbon_input = expected_c_p_to_soil + expected_c_e

    return {
        'calculator': calculator,
        'expected_c_p': expected_c_p,
        'expected_c_p_to_soil': expected_c_p_to_soil,
        'expected_c_s': expected_c_s,
        'expected_c_r': expected_c_r,
        'expected_c_e': expected_c_e,
        'expected_grain_n': expected_grain_n,
        'expected_straw_n': expected_straw_n,
        'expected_root_n': expected_root_n,
        'expected_exudate_n': expected_exudate_n,
        'expected_above_ground_residue_n': expected_above_ground_residue_n,
        'expected_below_ground_residue_n': expected_below_ground_residue_n,
        'expected_n_crop_residue': expected_n_crop_residue,
        'expected_above_ground_carbon_input': expected_above_ground_carbon_input,
        'expected_below_ground_carbon_input': expected_below_ground_carbon_input
    }

def test_wrong_type(test_data):
    data = test_data.copy()
    data['farm_data']['group'] = 123
    with pytest.raises(TypeError):
        CropResidueCalculator(data)

def test_negative_values(test_data):
    data = test_data.copy()
    data["farm_data"]['yield'] = -5
    with pytest.raises(ValueError):
        CropResidueCalculator(data)

def test_out_of_range_moisture(test_data):
    data = test_data.copy()
    data["crop_parameters"]['moisture'] = 110
    with pytest.raises(ValueError):
        CropResidueCalculator(data)

def test_c_p(setup):
    c_p = setup['calculator'].c_p()
    assert pytest.approx(c_p, 0.1) == setup['expected_c_p']

def test_c_p_to_soil(setup):
    c_p_to_soil = setup['calculator'].c_p_to_soil()
    assert pytest.approx(c_p_to_soil, 0.1) == setup['expected_c_p_to_soil']

def test_c_s(setup):
    c_s = setup['calculator'].c_s()
    assert pytest.approx(c_s, 0.1) == setup['expected_c_s']

def test_c_r(setup):
    c_r = setup['calculator'].c_r()
    assert pytest.approx(c_r, 0.1) == setup['expected_c_r']

def test_c_e(setup):
    c_e = setup['calculator'].c_e()
    assert pytest.approx(c_e, 0.1) == setup['expected_c_e']

def test_grain_n(setup):
    grain_n = setup['calculator'].grain_n()
    assert pytest.approx(grain_n, 0.1) == setup['expected_grain_n']

def test_straw_n(setup):
    straw_n = setup['calculator'].straw_n()
    assert pytest.approx(straw_n, 0.1) == setup['expected_straw_n']

def test_root_n(setup):
    root_n = setup['calculator'].root_n()
    assert pytest.approx(root_n, 0.1) == setup['expected_root_n']

def test_exudate_n(setup):
    exudate_n = setup['calculator'].exudate_n()
    assert pytest.approx(exudate_n, 0.1) == setup['expected_exudate_n']

def test_above_ground_residue_n(setup):
    above_ground_residue_n = setup['calculator'].above_ground_residue_n()
    assert pytest.approx(above_ground_residue_n, 0.1) == setup['expected_above_ground_residue_n']

def test_below_ground_residue_n(setup):
    below_ground_residue_n = setup['calculator'].below_ground_residue_n()
    assert pytest.approx(below_ground_residue_n, 0.1) == setup['expected_below_ground_residue_n']

def test_n_crop_residue(setup):
    n_crop_residue = setup['calculator'].n_crop_residue()
    assert pytest.approx(n_crop_residue, 0.1) == setup['expected_n_crop_residue']

def test_above_ground_carbon_input(setup):
    above_ground_carbon_input = setup['calculator'].above_ground_carbon_input()
    assert pytest.approx(above_ground_carbon_input, 0.1) == setup['expected_above_ground_carbon_input']

def test_below_ground_carbon_input(setup):
    below_ground_carbon_input = setup['calculator'].below_ground_carbon_input()
    assert pytest.approx(below_ground_carbon_input, 0.1) == setup['expected_below_ground_carbon_input']

def test_group_handling_annual(test_data):
    data = test_data.copy()
    data['farm_data']['group'] = 'annual'
    calculator = CropResidueCalculator(data)
    expected_above_ground = calculator.grain_n() + calculator.straw_n()
    expected_below_ground = calculator.root_n() + calculator.exudate_n()
    assert pytest.approx(calculator.above_ground_residue_n(), 0.2) == expected_above_ground
    assert pytest.approx(calculator.below_ground_residue_n(), 0.2) == expected_below_ground

def test_group_handling_perennial(test_data):
    data = test_data.copy()
    data['farm_data']['group'] = 'perennial'
    calculator = CropResidueCalculator(data)
    expected_above_ground = calculator.grain_n() + calculator.straw_n()
    expected_below_ground = calculator.root_n() * (data["crop_group_params"]['S_r'] / 100) + calculator.exudate_n()
    assert pytest.approx(calculator.above_ground_residue_n(), 0.2) == expected_above_ground
    assert pytest.approx(calculator.below_ground_residue_n(), 0.2) == expected_below_ground

def test_group_handling_root(test_data):
    data = test_data.copy()
    data['farm_data']['group'] = 'root'
    calculator = CropResidueCalculator(data)
    expected_above_ground = calculator.straw_n()
    expected_below_ground = calculator.grain_n() + calculator.exudate_n()
    assert pytest.approx(calculator.above_ground_residue_n(), 0.2) == expected_above_ground
    assert pytest.approx(calculator.below_ground_residue_n(), 0.2) == expected_below_ground

def test_group_handling_cover(test_data):
    data = test_data.copy()
    data['farm_data']['group'] = 'cover'
    calculator = CropResidueCalculator(data)
    expected_above_ground = calculator.grain_n()
    expected_below_ground = calculator.root_n() + calculator.exudate_n()
    assert pytest.approx(calculator.above_ground_residue_n(), 0.2) == expected_above_ground
    assert pytest.approx(calculator.below_ground_residue_n(), 0.2) == expected_below_ground

def test_group_handling_silage(test_data):
    data = test_data.copy()
    data['farm_data']['group'] = 'silage'
    calculator = CropResidueCalculator(data)
    expected_above_ground = calculator.grain_n()
    expected_below_ground = calculator.root_n() + calculator.exudate_n()
    assert pytest.approx(calculator.above_ground_residue_n(), 0.2) == expected_above_ground
    assert pytest.approx(calculator.below_ground_residue_n(), 0.2) == expected_below_ground

def test_get_crop_residue(setup):
    calculator = setup['calculator']
    result = calculator.get_crop_residue()
    expected_keys = [
        'C_p',
        'above_ground_carbon_input',
        'below_ground_carbon_input',
        'above_ground_residue_n',
        'below_ground_residue_n',
        'n_crop_residue'
    ]

    for key in expected_keys:
        assert key in result

    for key in expected_keys:
        assert isinstance(result[key], float)
