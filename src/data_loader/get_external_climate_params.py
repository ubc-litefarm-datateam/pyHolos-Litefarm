import sys
import os
import json
from datetime import datetime
from multiprocessing import Pool
import numpy as np
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.data_loader.evapotranspiration_calculator import EvapotranspirationCalculator


class ExternalClimateDataFetcher:
    """
    Facilitates the fetching and calculation of meteorological data for a series of 
    geographic points and a specified range of years of the growing season.

    Parameters
    ----------
    points : list of tuple
        A list of tuples, each representing the geographical coordinates (longitude, latitude).
    start_year : int
        The starting year of the period for which data is to be fetched.
    end_year : int
        The ending year of the period for which data is to be fetched.

    Attributes
    ----------
    base_url : str
        The base URL for the API from which the meteorological data is fetched.
    parameters : str
        A string listing the meteorological parameters to fetch from the API.
    community : str
        The community designation relevant to the API, defines the data set used.

    Methods
    -------
    fetch_data(point, year)
        Retrieves meteorological data from the API for a given point and year.

    calculate_totals(result)
        Calculates totals of precipitation and evapotranspiration from fetched data.

    process_points_over_years()
        Calculates average precipitation and evapotranspiration totals for multiple points across years.

    Examples
    --------
    >>> fetcher = ExternalClimateDataFetcher([(-93.6250, 42.0329)], 2020, 2021)
    >>> result = fetcher.process_points_over_years()
    >>> print(result)
    """

    def __init__(self, points, start_year, end_year):
        self.points = points
        self.start_year = start_year
        self.end_year = end_year
        self.base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
        self.parameters = "PRECTOTCORR,T2M,RH2M,ALLSKY_SFC_SW_DWN"
        self.community = "AG"

    def fetch_data(self, point, year):
        """
        Fetches meteorological data for a specified point and year using an API call.

        Parameters
        ----------
        point : tuple
            The geographic coordinates (longitude, latitude) for the data fetch.
        year : int
            The year for which the data is to be fetched.

        Returns
        -------
        dict
            A dictionary containing the success status, fetched data, or an error message.
        """
        longitude, latitude = point
        start_date = f"{year}0501"  # May 1st
        end_date = f"{year}0930"  # September 30th
        api_request_url = (
            f"{self.base_url}?parameters={self.parameters}&community={self.community}"
            f"&longitude={longitude}&latitude={latitude}&start={start_date}&end={end_date}&format=JSON"
        )

        # The request should be terminated if it takes longer than 60 seconds
        # to get a response from the server.
        try:
            response = requests.get(api_request_url, timeout=60.00)
            response.raise_for_status()
            return {
                "success": True,
                "data": json.loads(response.content.decode("utf-8")),
                "point": point,
                "year": year,
            }
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e), "point": point, "year": year}

    def calculate_totals(self, result):
        """
        Aggregates precipitation and calculates evapotranspiration over the growing season.

        Parameters
        ----------
        result : dict
            The result from `fetch_data` containing the success status, fetched data,
            or an error message.

        Returns
        -------
        dict
            A dictionary with the calculation results including success status,
            the calculated total precipitation and total evapotranspiration or
            an error message, and the corresponding point and year.
        """
        # response = self.fetch_growing_season_data()

        if not result["success"]:
            return result  # Return the error information directly

        data = result["data"]
        point = result["point"]
        year = result["year"]

        start_date = datetime.strptime(data["header"]["start"], "%Y%m%d")
        end_date = datetime.strptime(data["header"]["end"], "%Y%m%d")
        expected_days_count = (end_date - start_date).days + 1
        actual_days_count = len(data["properties"]["parameter"]["PRECTOTCORR"])

        # Check if the number of fetched days equals the number of expected days
        if actual_days_count != expected_days_count:
            return {
                "success": False,
                "error": "Incomplete data for the growing season.",
                "point": point,
                "year": year,
            }

        total_precipitation = 0
        total_evapotranspiration = 0

        for day in data["properties"]["parameter"]["PRECTOTCORR"]:
            total_precipitation += data["properties"]["parameter"]["PRECTOTCORR"][day]
            calculator = EvapotranspirationCalculator(
                mean_daily_temperature=data["properties"]["parameter"]["T2M"][day],
                solar_radiation=data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"][
                    day
                ],
                relative_humidity=data["properties"]["parameter"]["RH2M"][day],
            )
            daily_evapotranspiration = calculator.calculate()
            total_evapotranspiration += daily_evapotranspiration

        return {
            "success": True,
            "data": {"P": total_precipitation, "PE": total_evapotranspiration},
            "point": point,
            "year": year,
        }

    def process_points_over_years(self):
        """
        Processes multiple geographic points over a specified range of years to calculate 
        average total precipitation and evapotranspiration.

        Returns
        -------
        dict
            A dictionary mapping each point to its average precipitation and evapotranspiration 
            totals over the specified years, or an error message if applicable.
        """
        all_tasks = [
            (point, year)
            for point in self.points
            for year in range(self.start_year, self.end_year + 1)
        ]
        point_results = {}
        with Pool(min(5, len(self.points))) as pool:
            fetched_data = pool.starmap(self.fetch_data, all_tasks)
            calculated_totals = pool.map(self.calculate_totals, fetched_data)

        # Organize results by point and average across years
        for yearly_result in calculated_totals:
            point = yearly_result["point"]
            if yearly_result["success"]:
                if point not in point_results:
                    point_results[point] = {"P": [], "PE": [], "success": True}
                point_results[point]["P"].append(yearly_result["data"]["P"])
                point_results[point]["PE"].append(yearly_result["data"]["PE"])
            else:
                # If any year fails, record it and stop processing further years for this point
                point_results[point] = {
                    "error": yearly_result["error"],
                    "success": False,
                }
                # Remove P and PE records to emphasize failure
                point_results[point].pop("P", None)
                point_results[point].pop("PE", None)

        # Calculate averages only for points with all years successful
        for point, data in point_results.items():
            if data["success"]:
                data["P"] = np.round(np.mean(data["P"]), 2)
                data["PE"] = np.round(np.mean(data["PE"]), 2)
            else:
                # Ensure no misleading data is presented
                data.pop("P", None)
                data.pop("PE", None)

        return point_results


if __name__ == "__main__":
    test_points = [(-93.6250, 42.0329), (-89.3985, 43.0731)]  # Example list of points
    test_start_year = 2017
    test_end_year = 2021
    fetcher = ExternalClimateDataFetcher(test_points, test_start_year, test_end_year)
    averages = fetcher.process_points_over_years()
    print("Averages:", averages)
