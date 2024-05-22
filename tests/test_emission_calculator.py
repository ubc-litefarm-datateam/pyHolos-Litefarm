import unittest
from src.emission_calculator import EmissionCalculator

class TestEmissionCalculator(unittest.TestCase):

    def setUp(self):
        # Set up test data
        self.valid_ef_data = {
            'EF': 0.003286
        }
        self.valid_n_data = {
            'n_crop_residue': 560
        }
        self.invalid_ef_data_missing_key = {
            'EF_Topo': 0.0025
            # Missing 'EF'
        }
        self.invalid_ef_data_wrong_type = {
            'EF': '0.003286'  # Should be int/float
        }

    def test_valid_data(self):
        # Test with valid data
        calculator = EmissionCalculator(self.valid_ef_data, self.valid_n_data)
        n_crn_direct = calculator.calculate_n_crn_direct()
        n_crop_direct = calculator.calculate_n_crop_direct()
        no2_crop_direct = calculator.convert_n_crop_direct_to_n2o()
        co2_crop_direct = calculator.calculate_n2o_crop_direct_to_co2e()

        self.assertIsInstance(n_crn_direct, float)
        self.assertIsInstance(n_crop_direct, float)
        self.assertIsInstance(no2_crop_direct, float)
        self.assertIsInstance(co2_crop_direct, float)

    def test_missing_key(self):
        # Test with missing key
        with self.assertRaises(ValueError):
            EmissionCalculator(self.invalid_ef_data_missing_key, self.valid_n_data)

    def test_wrong_type(self):
        # Test with wrong data type
        with self.assertRaises(TypeError):
            EmissionCalculator(self.invalid_ef_data_wrong_type, self.valid_n_data)

    def test_intermediate_steps(self):
        # Test intermediate steps explicitly
        calculator = EmissionCalculator(self.valid_ef_data, self.valid_n_data)
        n_crn_direct = calculator.calculate_n_crn_direct()
        self.assertAlmostEqual(n_crn_direct, self.valid_n_data['n_crop_residue'] * self.valid_ef_data['EF'], places=5)

        calculator.calculate_n_other_direct()
        self.assertEqual(calculator.n_sn_direct, 0)
        self.assertEqual(calculator.n_crnmin_direct, 0)
        self.assertEqual(calculator.n_on_direct, 0)

        n_crop_direct = calculator.calculate_n_crop_direct()
        expected_n_crop_direct = 0 + 0 + 0 + n_crn_direct
        self.assertAlmostEqual(n_crop_direct, expected_n_crop_direct, places=5)

    def test_final_emission_calculations(self):
        # Test final emission calculations
        calculator = EmissionCalculator(self.valid_ef_data, self.valid_n_data)
        co2_crop_direct = calculator.calculate_n2o_crop_direct_to_co2e()

        n_crop_direct = calculator.calculate_n_crop_direct()
        no2_crop_direct = calculator.convert_n_crop_direct_to_n2o()
        expected_no2_crop_direct = n_crop_direct * (44 / 28)
        expected_co2_crop_direct = expected_no2_crop_direct * 273

        self.assertAlmostEqual(no2_crop_direct, expected_no2_crop_direct, places=5)
        self.assertAlmostEqual(co2_crop_direct, expected_co2_crop_direct, places=5)

if __name__ == '__main__':
    unittest.main()
