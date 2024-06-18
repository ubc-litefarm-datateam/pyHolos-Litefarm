"""
This module allows users to manage and store farm data. While we supports interactive 
prompts for entering farm data by running scripts `input_farm_record.py`, users can 
also directly add new farm records by modifying the predefined variables in this script. 

The script is designed to facilitate the easy addition of farm records with predefined 
data fields including farm ID, crop name, yield, area, geographical coordinates, and 
relevant year range. Adjust the data fields as necessary to record new farm data.
"""

from input_farm_record import *

# Add record, you can revise the following data
farm_id = "farm_0617_2"
common_crop_name = "Potato"
yield_kg = 5.17
area = 5000.0
latitude = 48.775
longitude = -72.688
start_year = 2020
end_year = 2020

new_farm_record = add_record(
    farm_id, common_crop_name, yield_kg, area, latitude, longitude, start_year, end_year
)
print(new_farm_record)
