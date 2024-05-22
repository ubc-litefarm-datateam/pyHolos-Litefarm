import unittest
import math
from src.emission_factor_calculator import EmissionFactorCalculator

class TestEmissionFactorCalculator(unittest.TestCase):

    def setUp(self):
        # Set up test data
        self.valid_data = {
            'climate_data' : {
                'P': 159,
                'PE': 678,
                'FR_Topo': 7.57
            },
            'modifiers' : {
                'RF_TX': 1,
                'RF_NS': 0.84,
                'RF_Till': 1,
                'RF_CS': 1,
                'RF_AM': 1
            }
        }
        self.invalid_data_missing_key = {
            'climate_data' : {
                'P': 159,
                'PE': 678,
                'FR_Topo': 7.57
            },
            'modifiers' : {
                'RF_TX': 1,
                'RF_NS': 0.84,
                'RF_Till': 1,
                'RF_AM': 1
            ## missing RF_CS
            }
        }
        self.invalid_data_wrong_type = {
            'climate_data' : {
                'P': '159', ## should be int/float
                'PE': 678,
                'FR_Topo': 7.57
            },
            'modifiers' : {
                'RF_TX': 1,
                'RF_NS': 0.84,
                'RF_Till': 1,
                'RF_CS': 1,
                'RF_AM': 1
            }
        }

    def test_valid_data(self):
        # Test with valid data
        calculator = EmissionFactorCalculator(self.valid_data)
        ef_ct_p, ef_ct_pe = calculator.calculate_ef_ct()
        ef_topo = calculator.calculate_ef_topo()
        ef = calculator.calculate_emission_factor()

        self.assertIsInstance(ef_ct_p, float)
        self.assertIsInstance(ef_ct_pe, float)
        self.assertIsInstance(ef_topo, float)
        self.assertIsInstance(ef, float)

    def test_missing_key(self):
        # Test with missing key
        with self.assertRaises(ValueError):
            EmissionFactorCalculator(self.invalid_data_missing_key)

    def test_wrong_type(self):
        # Test with wrong data type
        with self.assertRaises(TypeError):
            EmissionFactorCalculator(self.invalid_data_wrong_type)

    def test_intermediate_steps(self):
        # Test intermediate steps explicitly
        calculator = EmissionFactorCalculator(self.valid_data)
        ef_ct_p, ef_ct_pe = calculator.calculate_ef_ct()
        self.assertAlmostEqual(ef_ct_p, math.exp(0.00558 * self.valid_data['climate_data']['P'] - 7.7), places=5)
        self.assertAlmostEqual(ef_ct_pe, math.exp(0.00558 * self.valid_data['climate_data']['PE'] - 7.7), places=5)

        ef_topo = calculator.calculate_ef_topo()
        intermediate_factor = self.valid_data['climate_data']['P'] / self.valid_data['climate_data']['PE']
        if intermediate_factor > 1:
            self.assertEqual(ef_topo, ef_ct_p)
        elif self.valid_data['climate_data']['P'] == self.valid_data['climate_data']['PE']:
            self.assertEqual(ef_topo, ef_ct_pe)
        else:
            expected_ef_topo = ((ef_ct_pe * self.valid_data['climate_data']['FR_Topo'] / 100) + 
                                (ef_ct_p * (1 - self.valid_data['climate_data']['FR_Topo'] / 100)))
            self.assertAlmostEqual(ef_topo, expected_ef_topo, places=5)

    def test_final_emission_factor(self):
        # Test final emission factor calculation
        calculator = EmissionFactorCalculator(self.valid_data)
        ef = calculator.calculate_emission_factor()

        ef_ct_p, ef_ct_pe = calculator.calculate_ef_ct()
        ef_topo = calculator.calculate_ef_topo()
        ef_base = (ef_topo * self.valid_data['modifiers']['RF_TX']) * (1 / 0.645)
        expected_ef = ef_base * self.valid_data['modifiers']['RF_NS'] * self.valid_data['modifiers']['RF_Till'] * self.valid_data['modifiers']['RF_CS'] * self.valid_data['modifiers']['RF_AM']
        self.assertAlmostEqual(ef, expected_ef, places=5)

if __name__ == '__main__':
    unittest.main()
