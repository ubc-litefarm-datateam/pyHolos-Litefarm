"""
This module manages the recording and validation of farm data. Users can input data
regarding farm details which is then validated and stored in JSON format. Customize 
the output file name if necessary. The output path is pre-configured for consistency 
and should not be modified.

This script is designed for ease of use with interactive prompts for data entry and 
has  robust error handling to guide the user towards correct input formats.
"""

import os
import json
from datetime import datetime


def validate_inputs(
    farm_id, common_crop_name, yield_kg, area, latitude, longitude, start_year, end_year
):
    """
    Validate the inputs provided for adding a new farm record. Checks include data type validation and
    logical checks (e.g., year ranges).

    Parameters
    ----------
    farm_id : str
        Unique identifier for the farm.
    common_crop_name : str
        Name of the crop grown.
    yield_kg : float
        Yield of the crop in kilograms per square meter.
    area : float
        Area of the farm in square meters.
    latitude : float
        Geographic latitude of the farm.
    longitude : float
        Geographic longitude of the farm.
    start_year : int
        Starting year of the crop data record.
    end_year : int
        Ending year of the crop data record, must be less than the current year.

    Returns
    -------
    list
        A list of error messages, empty if no errors are found.
    """
    current_year = datetime.now().year
    errors = []
    if not isinstance(farm_id, str):
        errors.append("Farm ID must be a string.")
    if not isinstance(common_crop_name, str):
        errors.append("Common crop name must be a string.")
    if not isinstance(yield_kg, float):
        errors.append("Yield must be a float.")
    if not isinstance(area, float):
        errors.append("Area must be a float.")
    if not isinstance(latitude, float):
        errors.append("Latitude must be a float.")
    if not isinstance(longitude, float):
        errors.append("Longitude must be a float.")
    if not isinstance(start_year, int) or start_year <= 1984:
        errors.append("Start year must be an integer greater than 1984.")
    if not isinstance(end_year, int) or end_year >= current_year:
        errors.append("End year must be an integer less than the current year.")

    return errors


def add_record(
    farm_id, common_crop_name, yield_kg, area, latitude, longitude, start_year, end_year
):
    """
    Add a farm record to the JSON file after validating the inputs. If errors are found 
    in validation, they are returned and the record is not added.

    Parameters
    ----------
    farm_id : str
        Unique identifier for the farm.
    common_crop_name : str
        Name of the crop grown.
    yield_kg : float
        Yield of the crop in kilograms per square meter.
    area : float
        Area of the farm in square meters.
    latitude : float
        Geographic latitude of the farm.
    longitude : float
        Geographic longitude of the farm.
    start_year : int
        Starting year of the crop data record.
    end_year : int
        Ending year of the crop data record.

    Returns
    -------
    str
        Success message if the record is added successfully, otherwise returns error messages.
    """
    errors = validate_inputs(
        farm_id,
        common_crop_name,
        yield_kg,
        area,
        latitude,
        longitude,
        start_year,
        end_year,
    )
    if errors:
        return "Error: " + "; ".join(errors)

    record = {
        "area_in_m2": area,
        "latitude": latitude,
        "longitude": longitude,
        "common_crop_name": common_crop_name,
        "yield_kg_per_m2": yield_kg,
        "start_year": start_year,
        "end_year": end_year,
    }

    dir_path = os.path.dirname(os.path.realpath(__file__))
    output_path = os.path.join(dir_path, "..", "data", "test", "user_input_farm.json")

    try:
        with open(output_path, "r+") as file:
            data = json.load(file)
            data[farm_id] = record
            file.seek(0)
            json.dump(data, file, indent=4)
    except FileNotFoundError:
        with open(output_path, "w") as file:
            json.dump({farm_id: record}, file, indent=4)

    return "Record added successfully."


def main():
    """
    Main function to handle user interaction for entering farm data. It prompts the user 
    for all required fields, handles conversion of input to appropriate data types, and 
    provides feedback on the success or failure of data recording based on the validation.

    Returns
    -------
    None
    """
    print("Enter the farm data:")
    farm_id = input("Farm ID: ")
    common_crop_name = input("Common Crop Name: ")
    try:
        yield_kg = float(input("Yield (kg per m^2): "))
        area = float(input("Area (m^2): "))
        latitude = float(input("Latitude: "))
        longitude = float(input("Longitude: "))
        start_year = int(input("Start Year: "))
        end_year = int(input("End Year: "))
        result = add_record(
            farm_id,
            common_crop_name,
            yield_kg,
            area,
            latitude,
            longitude,
            start_year,
            end_year,
        )
        print(result)
    except ValueError as e:
        print(f"Invalid input, please enter the correct data types. {str(e)}")


if __name__ == "__main__":
    main()
