import unittest
from src.crop_residue_calculator import CropResidueCalculator

class TestCropResidueCalculator(unittest.TestCase):
    def setUp(self):
        self.farm_data = {
            # this test data is consistent with Holos 4 results: c_p, above_ground_carbon_input, below_ground_carbon_input
            # Suger Beets            
            "group": "root",
            "yield": 5000,
            "carbon_concentration": 0.45,
            "moisture": 80,
            "area": 10,
            "S_p": 0,
            "S_s": 100,
            "S_r": 100,
            "R_p": 0.626,
            "R_s": 0.357,
            "R_r": 0.01,
            "R_e": 0.007,
            "N_p": 10,
            "N_s": 29,
            "N_r": 10,
            "N_e": 10
        }

        self.calculator = CropResidueCalculator(self.farm_data)
        self.expected_c_p = 449.9999999999999
        self.expected_c_p_to_soil = 0.0
        self.expected_c_s = 256.629392971246 
        self.expected_c_r = 7.188498402555909
        self.expected_c_e = 5.031948881789136
        self.expected_grain_n = 0.0
        self.expected_straw_n = 16.538338658146962
        self.expected_root_n = 0.15974440894568687
        self.expected_exudate_n = 0.1118210862619808
        self.expected_above_ground_residue_n = 16.538338658146962
        self.expected_below_ground_residue_n = 0.1118210862619808
        self.expected_n_crop_residue = 166.5015974440894
        self.expected_above_ground_carbon_input = 256.629392971246
        self.expected_below_ground_carbon_input = 5.031948881789136


    def test_wrong_type(self):
        data = self.farm_data.copy()
        data['group'] = 123
        with self.assertRaises(TypeError):
            CropResidueCalculator(data)

    def test_negative_values(self):
        data = self.farm_data.copy()
        data['area'] = -5
        with self.assertRaises(ValueError):
            CropResidueCalculator(data)

    def test_out_of_range_moisture(self):
        data = self.farm_data.copy()
        data['moisture'] = 110
        with self.assertRaises(ValueError):
            CropResidueCalculator(data)


    def test_c_p(self):
        c_p = self.calculator.c_p()
        self.assertAlmostEqual(c_p, self.expected_c_p, places=1)

    def test_c_p_to_soil(self):
        c_p_to_soil = self.calculator.c_p_to_soil()
        self.assertAlmostEqual(c_p_to_soil, self.expected_c_p_to_soil, places=1)

    def test_c_s(self):
        c_s = self.calculator.c_s()
        self.assertAlmostEqual(c_s, self.expected_c_s, places=1)

    def test_c_r(self):
        c_r = self.calculator.c_r()
        self.assertAlmostEqual(c_r, self.expected_c_r, places=1)

    def test_c_e(self):
        c_e = self.calculator.c_e()
        self.assertAlmostEqual(c_e, self.expected_c_e, places=1)

    def test_grain_n(self):
        grain_n = self.calculator.grain_n()
        self.assertAlmostEqual(grain_n, self.expected_grain_n, places=1)

    def test_straw_n(self):
        straw_n = self.calculator.straw_n()
        self.assertAlmostEqual(straw_n, self.expected_straw_n, places=1)

    def test_root_n(self):
        root_n = self.calculator.root_n()
        self.assertAlmostEqual(root_n, self.expected_root_n, places=1)

    def test_exudate_n(self):
        exudate_n = self.calculator.exudate_n()
        self.assertAlmostEqual(exudate_n, self.expected_exudate_n, places=1)

    def test_above_ground_residue_n(self):
        above_ground_residue_n = self.calculator.above_ground_residue_n()
        self.assertAlmostEqual(above_ground_residue_n, self.expected_above_ground_residue_n, places=1)

    def test_below_ground_residue_n(self):
        below_ground_residue_n = self.calculator.below_ground_residue_n()
        self.assertAlmostEqual(below_ground_residue_n, self.expected_below_ground_residue_n, places=1)

    def test_n_crop_residue(self):
        n_crop_residue = self.calculator.n_crop_residue()
        self.assertAlmostEqual(n_crop_residue, self.expected_n_crop_residue, places=1)

    def test_above_ground_carbon_input(self):
        above_ground_carbon_input = self.calculator.above_ground_carbon_input()
        self.assertAlmostEqual(above_ground_carbon_input, self.expected_above_ground_carbon_input, places=1)

    def test_below_ground_carbon_input(self):
        below_ground_carbon_input = self.calculator.below_ground_carbon_input()
        self.assertAlmostEqual(below_ground_carbon_input, self.expected_below_ground_carbon_input, places=1)

    def test_group_handling_annual(self):
        data = self.farm_data.copy()
        data['group'] = 'annual'
        calculator = CropResidueCalculator(data)
        expected_above_ground = calculator.grain_n() + calculator.straw_n()
        expected_below_ground = calculator.root_n() + calculator.exudate_n()
        self.assertAlmostEqual(calculator.above_ground_residue_n(), expected_above_ground, places=2)
        self.assertAlmostEqual(calculator.below_ground_residue_n(), expected_below_ground, places=2)

    def test_group_handling_perennial(self):
        data = self.farm_data.copy()
        data['group'] = 'perennial'
        calculator = CropResidueCalculator(data)
        expected_above_ground = calculator.grain_n() + calculator.straw_n()
        expected_below_ground = calculator.root_n() * (data['S_r'] / 100) + calculator.exudate_n()
        self.assertAlmostEqual(calculator.above_ground_residue_n(), expected_above_ground, places=2)
        self.assertAlmostEqual(calculator.below_ground_residue_n(), expected_below_ground, places=2)

    def test_group_handling_root(self):
        data = self.farm_data.copy()
        data['group'] = 'root'
        calculator = CropResidueCalculator(data)
        expected_above_ground = calculator.straw_n()
        expected_below_ground = calculator.grain_n() + calculator.exudate_n()
        self.assertAlmostEqual(calculator.above_ground_residue_n(), expected_above_ground, places=2)
        self.assertAlmostEqual(calculator.below_ground_residue_n(), expected_below_ground, places=2)

    def test_group_handling_cover(self):
        data = self.farm_data.copy()
        data['group'] = 'cover'
        calculator = CropResidueCalculator(data)
        expected_above_ground = calculator.grain_n()
        expected_below_ground = calculator.root_n() + calculator.exudate_n()
        self.assertAlmostEqual(calculator.above_ground_residue_n(), expected_above_ground, places=2)
        self.assertAlmostEqual(calculator.below_ground_residue_n(), expected_below_ground, places=2)

    def test_group_handling_silage(self):
        data = self.farm_data.copy()
        data['group'] = 'silage'
        calculator = CropResidueCalculator(data)
        expected_above_ground = calculator.grain_n()
        expected_below_ground = calculator.root_n() + calculator.exudate_n()
        self.assertAlmostEqual(calculator.above_ground_residue_n(), expected_above_ground, places=2)
        self.assertAlmostEqual(calculator.below_ground_residue_n(), expected_below_ground, places=2)

if __name__ == "__main__":
    unittest.main()
