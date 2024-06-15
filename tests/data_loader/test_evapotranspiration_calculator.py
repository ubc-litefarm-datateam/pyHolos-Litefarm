"""
Module to test the EvapotranspirationCalculator functionality under various conditions.
"""

import pytest
from src.data_loader.evapotranspiration_calculator import EvapotranspirationCalculator


def test_calculate_positive_conditions():
    """Test evapotranspiration calculation with normal conditions to verify expected output."""
    calculator = EvapotranspirationCalculator(25.0, 5.0, 45)
    result = calculator.calculate()
    assert result == pytest.approx(
        1.47, rel=1e-2
    ), "The calculation does not match expected output"


def test_calculate_negative_temperature():
    """Test evapotranspiration calculation with negative temperature to ensure it returns zero."""
    calculator = EvapotranspirationCalculator(-1, 5.0, 45)
    result = calculator.calculate()
    assert result == 0, "Should return 0 for temperatures below or equal to 0"


def test_calculate_boundary_temperature():
    """Ensure the calculator handles extreme low temperatures properly by returning zero."""
    calculator = EvapotranspirationCalculator(-15, 5.0, 45)
    result = calculator.calculate()
    assert result == 0, "Should handle boundary condition of -15 degrees without error"


def test_calculate_high_humidity():
    """Test the calculator with high humidity to confirm positive evapotranspiration values."""
    calculator = EvapotranspirationCalculator(25.0, 5.0, 80)
    result = calculator.calculate()
    assert result > 0, "Should calculate positive ET for high humidity"


def test_calculate_low_humidity():
    """Verify that low humidity conditions still result in positive evapotranspiration values."""
    calculator = EvapotranspirationCalculator(25.0, 5.0, 10)
    result = calculator.calculate()
    assert result > 0, "Should calculate positive ET even for low humidity"
