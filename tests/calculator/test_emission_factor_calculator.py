import pytest
import math
from src.calculator.emission_factor_calculator import EmissionFactorCalculator


@pytest.fixture
def valid_data():
    return {
        "climate_data": {"P": 159, "PE": 678, "FR_Topo": 7.57, "soil_texture": 1},
        "modifiers": {"RF_NS": 0.84, "RF_Till": 1, "RF_CS": 1, "RF_AM": 1},
    }


@pytest.fixture
def invalid_data_missing_key():
    return {
        "climate_data": {"P": 159, "PE": 678, "FR_Topo": 7.57, "soil_texture": 1},
        "modifiers": {"RF_NS": 0.84, "RF_Till": 1, "RF_AM": 1},  # missing 'RF_CS'
    }


@pytest.fixture
def invalid_data_wrong_type():
    return {
        "climate_data": {
            "P": "159",
            "PE": 678,
            "FR_Topo": 7.57,
            "soil_texture": 1,
        },  # 'P' should be int/float
        "modifiers": {"RF_NS": 0.84, "RF_Till": 1, "RF_CS": 1, "RF_AM": 1},
    }


def test_valid_data(valid_data):
    calculator = EmissionFactorCalculator(valid_data)
    ef_ct_p, ef_ct_pe = calculator.calculate_ef_ct()
    ef_topo = calculator.calculate_ef_topo()
    ef = calculator.calculate_emission_factor()

    assert isinstance(ef_ct_p, float)
    assert isinstance(ef_ct_pe, float)
    assert isinstance(ef_topo, float)
    assert isinstance(ef, float)


def test_missing_key(invalid_data_missing_key):
    with pytest.raises(ValueError):
        EmissionFactorCalculator(invalid_data_missing_key)


def test_wrong_type(invalid_data_wrong_type):
    with pytest.raises(TypeError):
        EmissionFactorCalculator(invalid_data_wrong_type)


def test_intermediate_steps(valid_data):
    calculator = EmissionFactorCalculator(valid_data)
    ef_ct_p, ef_ct_pe = calculator.calculate_ef_ct()
    assert math.isclose(
        ef_ct_p, math.exp(0.00558 * valid_data["climate_data"]["P"] - 7.7), abs_tol=1e-5
    )
    assert math.isclose(
        ef_ct_pe,
        math.exp(0.00558 * valid_data["climate_data"]["PE"] - 7.7),
        abs_tol=1e-5,
    )

    ef_topo = calculator.calculate_ef_topo()
    intermediate_factor = (
        valid_data["climate_data"]["P"] / valid_data["climate_data"]["PE"]
    )
    if intermediate_factor > 1:
        assert ef_topo == ef_ct_p
    elif valid_data["climate_data"]["P"] == valid_data["climate_data"]["PE"]:
        assert ef_topo == ef_ct_pe
    else:
        expected_ef_topo = (ef_ct_pe * valid_data["climate_data"]["FR_Topo"] / 100) + (
            ef_ct_p * (1 - valid_data["climate_data"]["FR_Topo"] / 100)
        )
        assert math.isclose(ef_topo, expected_ef_topo, abs_tol=1e-5)


def test_final_emission_factor(valid_data):
    calculator = EmissionFactorCalculator(valid_data)
    ef = calculator.calculate_emission_factor()

    ef_ct_p, ef_ct_pe = calculator.calculate_ef_ct()
    ef_topo = calculator.calculate_ef_topo()
    ef_base = (ef_topo * valid_data["climate_data"]["soil_texture"]) * (1 / 0.645)
    expected_ef = (
        ef_base
        * valid_data["modifiers"]["RF_NS"]
        * valid_data["modifiers"]["RF_Till"]
        * valid_data["modifiers"]["RF_CS"]
        * valid_data["modifiers"]["RF_AM"]
    )
    assert math.isclose(ef, expected_ef, abs_tol=1e-5)
