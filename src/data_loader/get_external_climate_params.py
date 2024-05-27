import numpy as np
import requests
import json
from datetime import datetime
from multiprocessing import Pool
from data_loader.evapotranspiration_calculator import EvapotranspirationCalculator
# from evapotranspiration_calculator import EvapotranspirationCalculator

class ExternalClimateDataFetcher:
    """
    Fetches meteorological data for a specific geographic point and year for the growing season,
    and calculates total precipitation and evapotranspiration.

    Parameters
    ----------
    point : tuple
        A tuple representing the geographical coordinates (longitude, latitude).
    year : int
        The year for which the growing season data is required.

    Attributes
    ----------
    longitude : float
        Longitude of the point.
    latitude : float
        Latitude of the point.
    year : int
        Year for which data is fetched.
    base_url : str
        Base URL for the API from which the data is fetched.
    parameters : str
        Meteorological parameters to fetch from the API.
    community : str
        The community for which the data is relevant (e.g., agriculture).
    start_date : str
        Start date of the growing season in 'YYYYMMDD' format.
    end_date : str
        End date of the growing season in 'YYYYMMDD' format.

    Methods
    -------
    fetch_growing_season_data()
        Fetches daily meteorological data for the specified location and time range from the API.
    calculate_growing_season_totals()
        Calculates total precipitation and evapotranspiration for the growing season.

    Examples
    --------
    >>> point = (-93.6250, 42.0329)
    >>> year = 2021
    >>> fetcher = GrowingSeasonExternalDataFetcher(point, year)
    >>> result = fetcher.calculate_growing_season_totals()
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
        Sends an API request to fetch meteorological data and handles potential errors.

        Returns
        -------
        dict
            A dictionary containing the 'success' status and the fetched data or an error message.
        """
        longitude, latitude = point
        start_date = f"{year}0501"  # May 1st
        end_date = f"{year}0930"    # September 30th
        api_request_url = (
            f"{self.base_url}?parameters={self.parameters}&community={self.community}" 
            f"&longitude={longitude}&latitude={latitude}&start={start_date}&end={end_date}&format=JSON"
        )

        # The request should be terminated if it takes longer than 30 seconds 
        # to get a response from the server.
        try:
            response = requests.get(api_request_url, timeout=60.00)
            response.raise_for_status()
            return {"success": True, "data": json.loads(response.content.decode('utf-8')),
                   "point": point, "year": year}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e), "point": point, "year": year}

    def calculate_totals(self, result):
        """
        Aggregates precipitation and calculates evapotranspiration over the growing season.

        Returns
        -------
        dict
            A dictionary with the calculation results including success status, the calculated
            total precipitation and total evapotranspiration or an error message.
        """
        # response = self.fetch_growing_season_data()

        if not result['success']:
            return result  # Return the error information directly

        data = result['data']
        point = result['point']
        year = result['year']

        start_date = datetime.strptime(data['header']['start'], "%Y%m%d")
        end_date = datetime.strptime(data['header']['end'], "%Y%m%d")
        expected_days_count = (end_date - start_date).days + 1
        actual_days_count = len(data['properties']['parameter']['PRECTOTCORR'])
        
        # Check if the number of fetched days equals the number of expected days
        if actual_days_count != expected_days_count:
            return {"success": False, 
                    "error": "Incomplete data for the growing season.",
                    "point": point,
                    "year": year}

        total_precipitation = 0
        total_evapotranspiration = 0

        for day in data['properties']['parameter']['PRECTOTCORR']:
            total_precipitation += data['properties']['parameter']['PRECTOTCORR'][day]
            calculator = EvapotranspirationCalculator(
                mean_daily_temperature=data['properties']['parameter']['T2M'][day],
                solar_radiation=data['properties']['parameter']['ALLSKY_SFC_SW_DWN'][day],
                relative_humidity=data['properties']['parameter']['RH2M'][day]
            )
            daily_evapotranspiration = calculator.calculate()
            total_evapotranspiration += daily_evapotranspiration

        return {
            "success": True,
            "data": {
                'P': total_precipitation,
                'PE': total_evapotranspiration
            },
            "point": point,
            "year": year
        }

    def process_points_over_years(self):
        all_tasks = [(point, year) for point in self.points for year in range(self.start_year,
                                                                              self.end_year + 1)]
        point_results = {}
        with Pool(min(5, len(self.points))) as pool:
            fetched_data = pool.starmap(self.fetch_data, all_tasks) 
            calculated_totals = pool.map(self.calculate_totals, fetched_data)

        # Organize results by point and average across years
        for yearly_result in calculated_totals:
            point = yearly_result['point']
            if yearly_result['success']:
                if point not in point_results:
                    point_results[point] = {'P': [], 'PE': [], 'success': True}
                point_results[point]['P'].append(yearly_result['data']['P'])
                point_results[point]['PE'].append(yearly_result['data']['PE'])
            else:
                # If any year fails, record it and stop processing further years for this point
                point_results[point] = {'error': yearly_result['error'], 'success': False}
                # Remove P and PE records to emphasize failure
                point_results[point].pop('P', None)
                point_results[point].pop('PE', None)
        
        # Calculate averages only for points with all years successful
        for point, data in point_results.items():
            if data['success']:
                data['P'] = np.round(np.mean(data['P']), 2)
                data['PE'] = np.round(np.mean(data['PE']), 2)
            else:
                # Ensure no misleading data is presented
                data.pop('P', None)
                data.pop('PE', None)

        return point_results

if __name__ == '__main__':
    points = [(-93.6250, 42.0329), (-89.3985, 43.0731)]  # Example list of points
    start_year = 2017
    end_year = 2021
    fetcher = ExternalClimateDataFetcher(points, start_year, end_year)
    averages = fetcher.process_points_over_years()
    print("Averages:", averages)