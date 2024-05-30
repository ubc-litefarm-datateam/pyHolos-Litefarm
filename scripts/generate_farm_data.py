from input_farm_record import *

# Add record, you can revise the following data
farm_id = "farm456"
common_crop_name = "Potato"
yield_kg = 10.0
area = 5000.0
latitude = 48.775
longitude = -72.688
start_year = 2020
end_year = 2021

new_farm_record = add_record(farm_id, common_crop_name, yield_kg, area, latitude, longitude, start_year, end_year)
print(new_farm_record)

