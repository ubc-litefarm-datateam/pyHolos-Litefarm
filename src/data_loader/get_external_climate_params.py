import requests
import json
from datetime import datetime
from data_loader.evapotranspiration_calculator import EvapotranspirationCalculator

class GrowingSeasonExternalDataFetcher:
    """
    A class to fetch growing season data using the NASA POWER API and calculate total evapotranspiration.
    
    Attributes
    ----------
    latitude : float
        Latitude of the location for which data is requested.
    longitude : float
        Longitude of the location for which data is requested.
    year : int
        Year for which the data is requested.
    """
    
    def __init__(self, latitude, longitude, year):
        """
        Initializes the GrowingSeasonDataFetcher with specified location and year.
        
        Parameters
        ----------
        latitude : float
            Latitude of the location.
        longitude : float
            Longitude of the location.
        year : int
            Year for which data is requested.
        """
        self.latitude = latitude
        self.longitude = longitude
        self.year = year
        self.base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
        self.parameters = "PRECTOTCORR,T2M,RH2M,ALLSKY_SFC_SW_DWN"
        self.community = "AG"
        self.start_date = f"{year}0501"  # May 1st
        self.end_date = f"{year}0930"    # September 30th

    def fetch_growing_season_data(self):
        """
        Fetches the daily weather data for the growing season from the NASA POWER API.
        
        Returns
        -------
        dict
            Dictionary containing daily weather data for the growing season.
        """
        api_request_url = (
            f"{self.base_url}?parameters={self.parameters}&community={self.community}" 
            f"&longitude={self.longitude}&latitude={self.latitude}&start={self.start_date}&end={self.end_date}&format=JSON"

        )

        # The request should be terminated if it takes longer than 30 seconds 
        # to get a response from the server.
        try:
            response = requests.get(api_request_url, timeout=30.00)
            response.raise_for_status()
            return {"success": True, "data": json.loads(response.content.decode('utf-8'))}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def calculate_growing_season_totals(self):
        """
        Calculates total precipitation and total evapotranspiration using the fetched data.
        
        Returns
        -------
        dict
            Dictionary containing total precipitation and total evapotranspiration for the growing season.
        """
        response = self.fetch_growing_season_data()

        if not response['success']:
            return response  # Return the error information directly

        # Calculate the total number of expected days from the growing season
        data = response['data']
        start_date = datetime.strptime(self.start_date, "%Y%m%d")
        end_date = datetime.strptime(self.end_date, "%Y%m%d")
        expected_days_count = (end_date - start_date).days + 1
        actual_days_count = len(data['properties']['parameter']['PRECTOTCORR'])
        
        # Check if the number of fetched days equals the number of expected days
        if actual_days_count != expected_days_count:
            return {"success": False, 
                    "error": "Incomplete data for the growing season."}

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
                'P': round(total_precipitation, 2),
                'PE': round(total_evapotranspiration, 2)
            }
        }

