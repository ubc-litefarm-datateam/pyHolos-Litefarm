import pytest
from src.emission_calculator import EmissionCalculator

@pytest.fixture
def valid_ef_data():
    return {'EF': 0.003286}

@pytest.fixture
def valid_n_data():
    return {'n_crop_residue': 560}

@pytest.fixture
def invalid_ef_data_missing_key():
    return {'EF_Topo': 0.0025}

@pytest.fixture
def invalid_ef_data_wrong_type():
    return {'EF': '0.003286'}

def test_valid_data(valid_ef_data, valid_n_data):
    calculator = EmissionCalculator(valid_ef_data, valid_n_data)
    n_crn_direct = calculator.calculate_n_crn_direct()
    n_crop_direct = calculator.calculate_n_crop_direct()
    no2_crop_direct = calculator.convert_n_crop_direct_to_n2o()
    co2_crop_direct = calculator.calculate_n2o_crop_direct_to_co2e()

    assert isinstance(n_crn_direct, float)
    assert isinstance(n_crop_direct, float)
    assert isinstance(no2_crop_direct, float)
    assert isinstance(co2_crop_direct, float)

def test_missing_key(invalid_ef_data_missing_key, valid_n_data):
    with pytest.raises(ValueError):
        EmissionCalculator(invalid_ef_data_missing_key, valid_n_data)

def test_wrong_type(invalid_ef_data_wrong_type, valid_n_data):
    with pytest.raises(TypeError):
        EmissionCalculator(invalid_ef_data_wrong_type, valid_n_data)

def test_intermediate_steps(valid_ef_data, valid_n_data):
    calculator = EmissionCalculator(valid_ef_data, valid_n_data)
    n_crn_direct = calculator.calculate_n_crn_direct()
    assert abs(n_crn_direct - valid_n_data['n_crop_residue'] * valid_ef_data['EF']) < 1e-5

    calculator.calculate_n_other_direct()
    assert calculator.n_sn_direct == 0
    assert calculator.n_crnmin_direct == 0
    assert calculator.n_on_direct == 0

    n_crop_direct = calculator.calculate_n_crop_direct()
    expected_n_crop_direct = 0 + 0 + 0 + n_crn_direct
    assert abs(n_crop_direct - expected_n_crop_direct) < 1e-5

def test_final_emission_calculations(valid_ef_data, valid_n_data):
    calculator = EmissionCalculator(valid_ef_data, valid_n_data)
    co2_crop_direct = calculator.calculate_n2o_crop_direct_to_co2e()

    n_crop_direct = calculator.calculate_n_crop_direct()
    no2_crop_direct = calculator.convert_n_crop_direct_to_n2o()
    expected_no2_crop_direct = n_crop_direct * (44 / 28)
    expected_co2_crop_direct = expected_no2_crop_direct * 273

    assert abs(no2_crop_direct - expected_no2_crop_direct) < 1e-5
    assert abs(co2_crop_direct - expected_co2_crop_direct) < 1e-5
