import unittest
from src.crop_residue_calculator import CropResidueCalculator
# run python -m unittest tests/test_crop_residue_calculator.py in the root folder
class TestCropResidueCalculator(unittest.TestCase):
    def setUp(self):
        self.test_data = {
            # this test data is consistent with Holos 4 results in c_p, above_ground_carbon_input, below_ground_carbon_input
            # Suger Beets            

            "farm_data": 
            {
                "area": 10,
                "yield": 5000
            },
            
            "crop_group_params": 
            {
                "group": "root",
                "carbon_concentration": 0.45,
                "S_p": 0,
                "S_s": 100,
                "S_r": 100
            },
            
            "crop_parameters":
            {
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

        self.calculator = CropResidueCalculator(self.test_data)
        self.expected_c_p = (self.test_data["farm_data"]['yield'] + self.test_data["farm_data"]['yield'] * self.test_data["crop_group_params"]['S_p'] / 100) * (1 - self.test_data["crop_parameters"]['moisture'] / 100) * self.test_data["crop_group_params"]["carbon_concentration"]
        self.expected_c_p_to_soil = self.expected_c_p * self.test_data["crop_group_params"]['S_p'] / 100
        self.expected_c_s = self.expected_c_p * (self.test_data["crop_parameters"]['R_s'] / self.test_data["crop_parameters"]['R_p']) * (self.test_data["crop_group_params"]['S_s'] / 100)
        self.expected_c_r = self.expected_c_p * (self.test_data["crop_parameters"]['R_r'] / self.test_data["crop_parameters"]['R_p']) * (self.test_data["crop_group_params"]['S_r'] / 100)
        self.expected_c_e = self.expected_c_p *  (self.test_data["crop_parameters"]['R_e'] / self.test_data["crop_parameters"]['R_p']) 
        self.expected_grain_n = (self.expected_c_p_to_soil / 0.45) * (self.test_data["crop_parameters"]['N_p'] / 1000)
        self.expected_straw_n = (self.expected_c_s / 0.45) * (self.test_data["crop_parameters"]['N_s'] / 1000)
        self.expected_root_n = (self.expected_c_r / 0.45) * (self.test_data["crop_parameters"]['N_r'] / 1000)
        self.expected_exudate_n = (self.expected_c_e / 0.45) * (self.test_data["crop_parameters"]['N_e'] / 1000)
        self.expected_above_ground_residue_n = self.expected_straw_n
        self.expected_below_ground_residue_n = self.expected_grain_n + self.expected_exudate_n 
        self.expected_n_crop_residue = (self.expected_above_ground_residue_n + self.expected_below_ground_residue_n ) * self.test_data["farm_data"]['area']
        self.expected_above_ground_carbon_input = self.expected_c_s
        self.expected_below_ground_carbon_input = self.expected_c_p_to_soil + self.expected_c_e


    def test_wrong_type(self):
        data = self.test_data.copy()
        data['crop_group_params']['group'] = 123
        with self.assertRaises(TypeError):
            CropResidueCalculator(data)

    def test_negative_values(self):
        data = self.test_data.copy()
        data["farm_data"]['yield'] = -5
        with self.assertRaises(ValueError):
            CropResidueCalculator(data)

    def test_out_of_range_moisture(self):
        data = self.test_data.copy()
        data["crop_parameters"]['moisture'] = 110
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
        data = self.test_data.copy()
        data['crop_group_params']['group'] = 'annual'
        calculator = CropResidueCalculator(data)
        expected_above_ground = calculator.grain_n() + calculator.straw_n()
        expected_below_ground = calculator.root_n() + calculator.exudate_n()
        self.assertAlmostEqual(calculator.above_ground_residue_n(), expected_above_ground, places=2)
        self.assertAlmostEqual(calculator.below_ground_residue_n(), expected_below_ground, places=2)

    def test_group_handling_perennial(self):
        data = self.test_data.copy()
        data['crop_group_params']['group'] = 'perennial'
        calculator = CropResidueCalculator(data)
        expected_above_ground = calculator.grain_n() + calculator.straw_n()
        expected_below_ground = calculator.root_n() * (data["crop_group_params"]['S_r'] / 100) + calculator.exudate_n()
        self.assertAlmostEqual(calculator.above_ground_residue_n(), expected_above_ground, places=2)
        self.assertAlmostEqual(calculator.below_ground_residue_n(), expected_below_ground, places=2)

    def test_group_handling_root(self):
        data = self.test_data.copy()
        data['crop_group_params']['group'] = 'root'
        calculator = CropResidueCalculator(data)
        expected_above_ground = calculator.straw_n()
        expected_below_ground = calculator.grain_n() + calculator.exudate_n()
        self.assertAlmostEqual(calculator.above_ground_residue_n(), expected_above_ground, places=2)
        self.assertAlmostEqual(calculator.below_ground_residue_n(), expected_below_ground, places=2)

    def test_group_handling_cover(self):
        data = self.test_data.copy()
        data['crop_group_params']['group'] = 'cover'
        calculator = CropResidueCalculator(data)
        expected_above_ground = calculator.grain_n()
        expected_below_ground = calculator.root_n() + calculator.exudate_n()
        self.assertAlmostEqual(calculator.above_ground_residue_n(), expected_above_ground, places=2)
        self.assertAlmostEqual(calculator.below_ground_residue_n(), expected_below_ground, places=2)

    def test_group_handling_silage(self):
        data = self.test_data.copy()
        data['crop_group_params']['group'] = 'silage'
        calculator = CropResidueCalculator(data)
        expected_above_ground = calculator.grain_n()
        expected_below_ground = calculator.root_n() + calculator.exudate_n()
        self.assertAlmostEqual(calculator.above_ground_residue_n(), expected_above_ground, places=2)
        self.assertAlmostEqual(calculator.below_ground_residue_n(), expected_below_ground, places=2)

    def test_get_crop_residue(self):
        data = self.test_data.copy()
        calculator = CropResidueCalculator(data)
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
            self.assertIn(key, result)
            
        for key in expected_keys:
            self.assertIsInstance(result[key], float)

if __name__ == "__main__":
    unittest.main()
