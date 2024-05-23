import unittest
import pandas as pd
import io 
from src.data_loader.crop_checker import CropChecker
# python -m unittest tests/test_crop_checker.py
class TestCropChecker(unittest.TestCase):
    
    def test_crop_exists(self):
        checker = CropChecker('Camelina')
        self.assertTrue(checker.crop_exists(), "Camelina should exist in the crop list")

        checker = CropChecker('Mustard')
        self.assertTrue(checker.crop_exists(), "Mustard should exist in the crop list")

    def test_crop_does_not_exist(self):
        checker = CropChecker('Orange')
        self.assertFalse(checker.crop_exists(), "Orange should not exist in the crop list")

        checker = CropChecker('Onion')
        self.assertFalse(checker.crop_exists(), "Onion should not exist in the crop list")

    def test_boolean(self):
        checker = CropChecker('Soybean')
        result = checker.crop_exists()
        self.assertIsInstance(result, bool, "The output should be a boolean")

if __name__ == '__main__':
    unittest.main()