class EvapotranspirationCalculator:
    """
    Class to calculate reference evapotranspiration using the Turc method.

    Attributes:
    mean_daily_temperature (float): Mean daily temperature in Celsius.
    solar_radiation (float): Solar radiation in MJ m^-2 day^-1.
    relative_humidity (float): Relative humidity in percent.
    """
    def __init__(self, mean_daily_temperature, solar_radiation, relative_humidity):
        """
        Initialize the EvapotranspirationCalculator with required parameters.
        """
        self.mean_daily_temperature = mean_daily_temperature
        self.solar_radiation = solar_radiation
        self.relative_humidity = relative_humidity

    def calculate(self):
        """
        Calculate the reference evapotranspiration based on initialized parameters.

        Returns:
        float: Reference evapotranspiration in mm day^-1.
        """
        # Holos Technical Report, Page 22:
            # Eq. 1.6.2-1
            # Eq. 1.6.2-2
                # Turc equation
        # Holos Github code:
            # https://github.com/holos-aafc/Holos/blob/afb61d2fe38e62a818c8b5932d308497da12a5da/H.Core/Calculators/Climate/EvapotranspirationCalculator.cs
    
        term1 = 0.013

        # Return 0 evapotranspiration if temperature is <= 0
        if self.mean_daily_temperature <= 0:
            return 0

        # Avoid division by zero if temperature exactly -15 degrees Celsius
        if abs(self.mean_daily_temperature + 15) < 1e-10:
            return 0

        term2 = self.mean_daily_temperature / (self.mean_daily_temperature + 15)
        term3 = (23.8856 * self.solar_radiation) + 50
        term4 = 1 + ((50 - self.relative_humidity) / 70)

        if self.relative_humidity >= 50:
            result = term1 * term2 * term3
        else:
            result = term1 * term2 * term3 * term4

        # Ensure evapotranspiration is not negative
        if result < 0:
            return 0

        return result

