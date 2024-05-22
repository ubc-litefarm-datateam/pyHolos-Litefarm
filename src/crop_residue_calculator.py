class CropResidueCalculator:
    """
    Calculator for estimating crop residue nitrogen content based on farm data.

    Attributes:
        area (float): Area of the farm in hectares (ha).
        group (str): Crop group (e.g., "annual", "perennial", "root", "cover", "silage").
        crop_yield (float): Yield of the crop in kg/ha.
        moisture (float): Moisture content of the crop as a percentage (%).
        carbon_concentration (float): Carbon concentration in the crop (kg kg-1).
        S_p, S_s, S_r (float): Percentage values for soil parameters (%).
        R_p, R_s, R_r, R_e (float): Residue fractions for various parts of the crop.
        N_p, N_s, N_r, N_e (float): Nitrogen content for various parts of the crop (kg/ha).
    """

    def __init__(self, farm_data):
        """
        Initializes the CropResidueCalculator with the provided farm data.

        Args:
            farm_data (dict): A dictionary containing farm data.

        """
        self.validate_input(farm_data)
        self.data = farm_data
        self.area = farm_data["area"]
        self.group = farm_data["group"]
        self.crop_yield = farm_data["yield"]
        self.moisture = farm_data["moisture"]
        self.carbon_concentration = farm_data["carbon_concentration"]
        # self.method = farm_data["method"]

        self.S_p = farm_data["S_p"]
        self.S_s = farm_data["S_s"]
        self.S_r = farm_data["S_r"]

        self.R_p = farm_data["R_p"]
        self.R_s = farm_data["R_s"]
        self.R_r = farm_data["R_r"]
        self.R_e = farm_data["R_e"]

        self.N_p = farm_data["N_p"]
        self.N_s = farm_data["N_s"]
        self.N_r = farm_data["N_r"]
        self.N_e = farm_data["N_e"]
    
    
    def validate_input(self, farm_data):
        """ Validates the input farm data to ensure all required fields are present and have the correct types and values. """
        
        if not isinstance(farm_data["group"], str):
            raise TypeError("group must be a string")
        if farm_data["group"] not in ["annual", "perennial", "root", "cover", "silage"]:
            raise ValueError("group must be one of 'annual', 'perennial', 'root', 'cover', 'silage'")
        
        
        for key in ["yield", "carbon_concentration", "moisture", "area", "S_p", "S_s", "S_r", "R_p", "R_s", "R_r", "R_e", "N_p", "N_s", "N_r", "N_e"]:
            if not isinstance(farm_data[key], (int, float)):
                raise TypeError(f"{key} must be a number")
        if farm_data["area"] < 0:
            raise ValueError("Area must be non-negative")
        if farm_data["yield"] < 0:
            raise ValueError("Yield must be non-negative")
        if not (0 <= farm_data["moisture"] <= 100):
            raise ValueError("Moisture must be between 0 and 100")

            
    def c_p(self):
        """
        Calculates the carbon input to the soil.

        Returns:
            float: The carbon input to the soil. 
        """
        if abs(self.S_p - 100) < 1e-5:
            return self.crop_yield * (1 - self.moisture / 100) * self.carbon_concentration      
        # if self.method in ["swathing", "greenmanure"]:
        #     return self.crop_yield * (1 - self.moisture / 100) * self.carbon_concentration
        return (self.crop_yield + self.crop_yield * self.S_p / 100) * (1 - self.moisture / 100) * self.carbon_concentration

   
    def c_p_to_soil(self):
        """
        Calculates the carbon input to the soil from the product.
        Formula: C_p_to_soil = C_p * S_p / 100

        Returns:
            float: Carbon input to the soil from the product.
        """
        return self.c_p() * (self.S_p / 100)
   
    def c_s(self):
        """
        Calculates the carbon input to the soil from the straw.
        Formula: C_s = C_p * (R_s / R_p) * (S_s / 100)

        Returns:
            float: Carbon input to the soil from the straw.
        """
        return self.c_p() * (self.R_s / self.R_p) * (self.S_s / 100)

    def c_r(self):
        """
        Calculates the carbon input to the soil from the roots.
        Fomula: C_r = C_p * (R_r / R_p) * (S_r / 100)
        
        Returns:
            float: Carbon input to the soil from the root.
        """
        return self.c_p() * (self.R_r / self.R_p) * (self.S_r / 100)
    
    def c_e(self):
        """
        Calculates the carbon input to the soil from the extra-roots.
        Fomula: C_e = C_p * (R_e / R_p)

        Returns:
            float: Carbon input to the soil from the extra-roots.
        """
        return self.c_p() * (self.R_e / self.R_p)
    
    def grain_n(self):
        """
        Calculates the nitrogen content of the grain returned to the soil.
        Fomula: Grain_n = C_p_to_soil / 0.45 * N_p / 1000

        Returns:
            float: The nitrogen content of the grain (kg N/ha).
        """
        return (self.c_p_to_soil() / 0.45) * (self.N_p / 1000)

    def straw_n(self):
        """
        Calculates the nitrogen content of the straw returned to the soil.
        Formula: Straw_n = C_s / 0.45 * N_s / 1000

        Returns:
            float: The nitrogen content of the straw (kg N/ha).
        """
        return (self.c_s() / 0.45) * (self.N_s / 1000)

    def root_n(self):
        """
        Calculates the nitrogen content of the roots returned to the soil.
        Formula: Root_n = C_r / 0.45 * N_r / 1000

        Returns:
            float: The nitrogen content of the roots (kg N/ha).
        """
        
        return (self.c_r() / 0.45) * (self.N_r / 1000)

    def exudate_n(self):
        """
        Calculates the nitrogen content of the exudates returned to the soil.
        Formula: Exudate_n = C_e / 0.45 * N_e / 1000

        Returns:
            float: The nitrogen content of the exudates (kg N/ha).
        """
        
        return (self.c_e() / 0.45) * (self.N_e / 1000)

    def above_ground_residue_n(self):
        """
        Calculates the total nitrogen content of the above-ground residue.

        Returns:
            float: The nitrogen content of the above-ground residue (kg N/ha).
        """
        if self.group in ["annual", "perennial"]:
            return self.grain_n() + self.straw_n()
        elif self.group == "root":
            return self.straw_n()
        elif self.group in ["cover", "silage"]:
            return self.grain_n()
        else:
            return 0

    def below_ground_residue_n(self):
        """
        Calculates the total nitrogen content of the below-ground residue.

        Returns:
            float: The nitrogen content of the below-ground residue (kg N/ha).
        """
        if self.group == "annual":
            return self.root_n() + self.exudate_n()
        elif self.group == "perennial":
            return self.root_n() * (self.S_r / 100) + self.exudate_n()
        elif self.group == "root":
            return self.grain_n() + self.exudate_n()
        elif self.group in ["cover", "silage"]:
            return self.root_n() + self.exudate_n()
        else:
            return 0

    def n_crop_residue(self):
        """
        Calculates the total nitrogen content of the crop residue.

        Formula:
        N_crop_residue = (above_ground_residue_n + below_ground_residue_n) * area

        Returns:
            float: The total nitrogen content of the crop residue (kg N).
        """
        return (self.above_ground_residue_n() + self.below_ground_residue_n()) * self.area


    def above_ground_carbon_input(self):
        """
        Calculates the above ground carbon input.

        Returns:
            float: Above ground carbon input.
        """
        # if self.method in ["greenmanure", "swathing"]:
        #     return self.c_p_to_soil()

        if self.group == "root":
            return self.c_s()

        return self.c_p_to_soil() + self.c_s()


        
    def below_ground_carbon_input(self):
        """
        Calculates the below ground carbon input.

        Returns:
            float: Below ground carbon input.
        """
        if self.group == "root":
            return self.c_p_to_soil() + self.c_e()
        else:
            return self.c_r() + self.c_e()


