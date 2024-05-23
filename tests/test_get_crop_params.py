import unittest
from src.data_loader.get_crop_params import CropParametersManager
from src.data_loader.get_farm_data import FarmData

# run command python -m unittest tests/test_get_crop_params.py in the root folder of the project
class TestCropParametersManager(unittest.TestCase):
    def setUp(self):
        
        self.validation_data = {
            'Soybean': {
                'moisture': 14,
                'R_p': 0.304,
                'R_s': 0.455,
                'R_r': 0.146,
                'R_e': 0.095,
                'N_p': 67.0,
                'N_s': 6.0,
                'N_r': 10.0,
                'N_e': 10.0
            },
            'Wheat_100': {
                'moisture': 12,
                'R_p': 0.219,
                'R_s': 0.551,
                'R_r': 0.136,
                'R_e': 0.095,
                'N_p': 27.9,
                'N_s': 8.6,
                'N_r': 13.4,
                'N_e': 13.4
            },
            'Wheat_300': {
                'moisture': 12,
                'R_p': 0.244,
                'R_s': 0.518,
                'R_r': 0.147,
                'R_e': 0.091,
                'N_p': 26.3,
                'N_s': 8.2,
                'N_r': 10.4,
                'N_e': 10.4
            },
            'Wheat_500': {
                'moisture': 12,
                'R_p': 0.431,
                'R_s': 0.488,
                'R_r': 0.049,
                'R_e': 0.032,
                'N_p': 56.2,
                'N_s': 6.5,
                'N_r': 11.9,
                'N_e': 11.9
            },
            'Oilseeds_rainfed': {
                'moisture': 9,
                'R_p': 0.184,
                'R_s': 0.637,
                'R_r': 0.109,
                'R_e': 0.071,
                'N_p': 61.5,
                'N_s': 7.0,
                'N_r': 10.0,
                'N_e': 10.0
            },
            'Oilseeds_irrigated': {
                'moisture': 9,
                'R_p': 0.213,
                'R_s': 0.619,
                'R_r': 0.101,
                'R_e': 0.066,
                'N_p': 61.5,
                'N_s': 7.0,
                'N_r': 10.0,
                'N_e': 10.0
            }
        }
        self.farm_data = FarmData("0369f026-1f90-11ee-b788-0242ac150004")

    def check_crop_parameters(self, farm_data, climate_data, expected):
        manager = CropParametersManager(farm_data, climate_data)
        crop_parameters = manager.get_crop_parameters()
        self.assertEqual(crop_parameters, expected)

    def test_crop_names(self):
        self.farm_data.farm_data['crop'] = 'Soybean'
        climate_data = {'P': 100, 'PE': 150}
        self.check_crop_parameters(self.farm_data, climate_data, self.validation_data['Soybean'])
        
    def test_condition_irrigated(self):
        self.farm_data.farm_data['crop'] = 'Oilseeds'
        climate_data = {'P': 100, 'PE': 150}
        self.check_crop_parameters(self.farm_data, climate_data, self.validation_data['Oilseeds_irrigated'])
    
    def test_condition_rainfed(self):
        self.farm_data.farm_data['crop'] = 'Oilseeds'
        climate_data = {'P': 200, 'PE': 150}
        self.check_crop_parameters(self.farm_data, climate_data, self.validation_data['Oilseeds_rainfed'])

    def test_condition_low(self):
        self.farm_data.farm_data['crop'] = 'Wheat'
        climate_data = {'P': 100, 'PE': 200}
        self.check_crop_parameters(self.farm_data, climate_data, self.validation_data['Wheat_100'])
        
    def test_condition_middle(self):
        self.farm_data.farm_data['crop'] = 'Wheat'
        climate_data = {'P': 100, 'PE': 400}
        self.check_crop_parameters(self.farm_data, climate_data, self.validation_data['Wheat_300'])

    def test_condition_great(self):
        self.farm_data.farm_data['crop'] = 'Wheat'
        climate_data = {'P': 100, 'PE': 600}
        self.check_crop_parameters(self.farm_data, climate_data, self.validation_data['Wheat_500'])

    def test_output_keys(self):
        self.farm_data.farm_data['crop'] = 'Wheat'
        climate_data = {'P': 100, 'PE': 600}
        crop_parameters = CropParametersManager(self.farm_data, climate_data).get_crop_parameters()
        expected_keys = [
            'moisture',
            'R_p',
            'R_s',
            'R_r',
            'R_e',
            'N_p',
            'N_s',
            'N_r',
            'N_e',
        ]

        for key in expected_keys:
            self.assertIn(key, crop_parameters)


if __name__ == "__main__":
    unittest.main()