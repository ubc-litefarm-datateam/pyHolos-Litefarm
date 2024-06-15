class CropResidueCalculator:
    """
    Calculator for estimating crop residue nitrogen content based on farm data.

    Attributes
    ----------
    area : float
        Area of the farm in hectares (ha).
    group : str
        Crop group (e.g., "annual", "perennial", "root", "cover", "silage").
    crop_yield : float
        Yield of the crop in kg/ha.
    moisture : float
        Moisture content of the crop as a percentage (%).
    carbon_concentration : float
        Carbon concentration in the crop (kg kg-1).
    S_p, S_s, S_r : float
        Percentage of product/straw/roots yield returned to soil (%).
    R_p, R_s, R_r, R_e : float
        Relative biomass allocation coefficient for product/straw/roots/extra-root material.
    N_p, N_s, N_r, N_e : float
        Nitrogen content for various parts of the crop (kg/ha).

    
    Methods
    -------
    validate_input(data):
        Validates the input farm data to ensure all required fields are present and have the correct types and values.
    c_p():
        Calculates the plant carbon in agricultural product (kg ha-1).
    c_p_to_soil():
        Calculates the carbon input from the product (kg ha-1).
    c_s():
        Calculates the carbon input from the straw (kg ha-1).
    c_r():
        Calculates the carbon input from the roots (kg ha-1).
    c_e():
        Calculates the carbon input from the extra-roots (kg ha-1).
    grain_n():
        Calculates the nitrogen content of the grain returned to the soil (kg N ha-1).
    straw_n():
        Calculates the nitrogen content of the straw returned to the soil (kg N ha-1).
    root_n():
        Calculates the nitrogen content of the root returned to the soil (kg N ha-1) 
    exudate_n():
        Calculates the nitrogen content of the exudates returned to the soil (kg N ha-1).
    above_ground_residue_n():
        Calculates the aboveground residue N (kg N ha-1).
    below_ground_residue_n():
        Calculates the belowground residue N (kg N ha-1).
    n_crop_residue():
        Calculates the nitrogen inputs from crop residue returned to soil (kg N).
    above_ground_carbon_input():
        Calculates the aboveground residue C input (kg ha-1).
    below_ground_carbon_input():
        Calculates the belowground residue C input (kg ha-1).
    get_crop_residue():
        Calculates and returns crop residue results.

    Examples
    --------
    >>> data = {
    ...     "farm_data": {"area": 10, "yield": 5000},
    ...     "crop_group_params": {"group": "annual", "carbon_concentration": 0.45, "S_p": 30, "S_s": 20, "S_r": 10},
    ...     "crop_parameters": {"moisture": 15, "R_p": 1.0, "R_s": 0.5, "R_r": 0.3, "R_e": 0.2, "N_p": 12, "N_s": 5, "N_r": 3, "N_e": 2}
    ... }
    >>> calc = CropResidueCalculator(data)
    >>> calc.n_crop_residue()
    25.166666666666668
    >>> calc.get_crop_residue()
    {'C_p': 1912.5, 'above_ground_carbon_input': 764.25, 'below_ground_carbon_input': 955.25, 'above_ground_residue_n': 17.77777777777778, 'below_ground_residue_n': 7.388888888888889, 'n_crop_residue': 25.166666666666668}
    """

    def __init__(self, data):
        """
        Initializes the CropResidueCalculator with the provided farm data.

        Parameters
        ----------
        data : dict
            A dictionary containing farm data.
        """
        
        self.validate_input(data)
        self.data = data
        self.area = data["farm_data"]["area"]
        self.group = data["farm_data"]["group"].lower()
        self.crop_yield = data["farm_data"]["yield"]
        self.moisture = data["crop_parameters"]["moisture"]
        self.carbon_concentration = data["crop_group_params"]["carbon_concentration"]

        self.S_p = data["crop_group_params"]["S_p"]
        self.S_s = data["crop_group_params"]["S_s"]
        self.S_r = data["crop_group_params"]["S_r"]

        self.R_p = data["crop_parameters"]["R_p"]
        self.R_s = data["crop_parameters"]["R_s"]
        self.R_r = data["crop_parameters"]["R_r"]
        self.R_e = data["crop_parameters"]["R_e"]

        self.N_p = data["crop_parameters"]["N_p"]
        self.N_s = data["crop_parameters"]["N_s"]
        self.N_r = data["crop_parameters"]["N_r"]
        self.N_e = data["crop_parameters"]["N_e"]
    
    
    def validate_input(self, data):
        """ Validates the input farm data to ensure all required fields are present and have the correct types and values. """
        
        if not isinstance(data["farm_data"]["group"], str):
            raise TypeError("group must be a string")
       
        if data["farm_data"]["group"].lower() not in ["annual", "perennial", "root", "cover", "silage"]:
            raise ValueError("group must be one of 'annual', 'perennial', 'root', 'cover', 'silage'")
        
        if data["farm_data"]["area"] < 0:
            raise ValueError("Area must be non-negative")
        
        if data["farm_data"]["yield"] < 0:
            raise ValueError("Yield must be non-negative")
        
        if not (0 <= data["crop_parameters"]["moisture"] <= 100):
            raise ValueError("Moisture must be between 0 and 100")

            
    def c_p(self):
        """"
        Calculates the plant carbon in agricultural product (kg ha-1).
        Equation 2.1.2-1 in the Holos version 4.0 algorithm document.    

        Returns
        -------
        float
            The plant carbon in agricultural product (kg ha-1).
        """
       
        if abs(self.S_p - 100) < 1e-5:
            self.C_p = self.crop_yield * (1 - self.moisture / 100) * self.carbon_concentration
        else:
            self.C_p = (self.crop_yield + self.crop_yield * self.S_p / 100) * (1 - self.moisture / 100) * self.carbon_concentration
        
        return self.C_p

   
    def c_p_to_soil(self):
        """
        Calculates the carbon input from the product.
        Equation 2.1.2-6, 2.1.2-10, 2.1.2-14 and 2.1.2-17 in the Holos version 4.0 algorithm document.  

        Returns
        -------
        float
            Carbon input from the product (kg ha-1).
        """
       
        self.C_p_to_soil = self.c_p() * (self.S_p / 100)
        
        return self.C_p_to_soil
   
    def c_s(self):
        """
        Calculates the carbon input from the straw.
        Equation 2.1.2-7 and 2.1.2-18 in the Holos version 4.0 algorithm document.  

        Returns
        -------
        float
            Carbon input from the straw (kg ha-1).
        """
        
        if abs(self.R_p) < 1e-6:
            self.C_s = 0
        else:
            self.C_s = self.c_p() * (self.R_s / self.R_p) * (self.S_s / 100)
        
        return self.C_s

    def c_r(self):
        """
        Calculates the carbon input from the roots.
        Equation 2.1.2-8, 2.1.2-11 and 2.1.2-15 in the Holos version 4.0 algorithm document.  

        Returns
        -------
        float
            Carbon input from the roots (kg ha-1).
        """
        
        if abs(self.R_p) < 1e-6:
            self.C_r = 0
        else:
            self.C_r = self.c_p() * (self.R_r / self.R_p) * (self.S_r / 100)
        
        return self.C_r
    
    def c_e(self):
        """
        Calculates the carbon input from the extra-roots.
        Equation 2.1.2-9, 2.1.2-12, 2.1.2-16 and 2.1.2-19 in the Holos version 4.0 algorithm document.  

        Returns
        -------
        float
            Carbon input from the extra-roots (kg ha-1).
        """
        
        if abs(self.R_p) < 1e-6:
            self.C_e = 0
        else:
            self.C_e = self.c_p() * (self.R_e / self.R_p)
        
        return self.C_e
    
    def grain_n(self):
        """
        Calculates the nitrogen content of the grain returned to the soil.
        Equation 2.5.6-2 in the Holos version 4.0 algorithm document.  

        Returns
        -------
        float
            The nitrogen content of the grain (kg N ha -1).
        """
        
        self.Grain_N = (self.c_p_to_soil() / 0.45) * (self.N_p / 1000)
        
        return self.Grain_N

    def straw_n(self):
        """
        Calculates the nitrogen content of the straw returned to the soil.
        Equation 2.5.6-3 in the Holos version 4.0 algorithm document.  

        Returns
        -------
        float
            The nitrogen content of the straw (kg N ha -1).
        """
        
        self.Straw_N = (self.c_s() / 0.45) * (self.N_s / 1000)
        
        return self.Straw_N

    def root_n(self):
        """
        Calculates the nitrogen content of the roots returned to the soil.
        Equation 2.5.6-4 in the Holos version 4.0 algorithm document. 

        Returns
        -------
            float: The nitrogen content of the roots (kg N ha -1).
        """
        
        self.Root_N = (self.c_r() / 0.45) * (self.N_r / 1000)
        
        return self.Root_N

    def exudate_n(self):
        """
        Calculates the nitrogen content of the exudates returned to the soil.
        Equation 2.5.6-5 in the Holos version 4.0 algorithm document. 

        Returns
        -------
            float: The nitrogen content of the exudates (kg N ha -1).
        """
       
        self.Exudate_N = (self.c_e() / 0.45) * (self.N_e / 1000)
        
        return self.Exudate_N

    def above_ground_residue_n(self):
        """
        Calculates the total nitrogen content of the above-ground residue.
        Equation 2.5.6-6 in the Holos version 4.0 algorithm document. 

        Returns
        -------
            float: The nitrogen content of the above-ground residue (kg N ha-1).
        """
       
        if self.group in ["annual", "perennial"]:
            self.Above_Ground_Residue_N = self.grain_n() + self.straw_n()
        elif self.group == "root":
            self.Above_Ground_Residue_N = self.straw_n()
        elif self.group in ["cover", "silage"]:
            self.Above_Ground_Residue_N = self.grain_n()
        else:
            self.Above_Ground_Residue_N = 0
        
        return self.Above_Ground_Residue_N

    def below_ground_residue_n(self):
        """
        Calculates the total nitrogen content of the below-ground residue.
        Equation 2.5.6-6 and 2.5.6-7 in the Holos version 4.0 algorithm document. 

        Returns
        -------
            float: The nitrogen content of the below-ground residue (kg N ha-1).
        """
       
        if self.group == "annual":
            self.Below_Ground_Residue_N = self.root_n() + self.exudate_n()
        elif self.group == "perennial":
            self.Below_Ground_Residue_N = self.root_n() * (self.S_r / 100) + self.exudate_n()
        elif self.group == "root":
            self.Below_Ground_Residue_N = self.grain_n() + self.exudate_n()
        elif self.group in ["cover", "silage"]:
            self.Below_Ground_Residue_N = self.root_n() + self.exudate_n()
        else:
            self.Below_Ground_Residue_N = 0
        
        return self.Below_Ground_Residue_N

    def n_crop_residue(self):
        """
        Calculates the total nitrogen content of the crop residue.
        Equation 2.5.6-9 in the Holos version 4.0 algorithm document. 

        Returns
        -------
            float: The total nitrogen content of the crop residue (kg N).
        """
        
        self.N_Crop_Residue = (self.above_ground_residue_n() + self.below_ground_residue_n()) * self.area
        
        return self.N_Crop_Residue


    def above_ground_carbon_input(self):
        """
        Calculates the above ground carbon input.
        Equation 2.1.2-2 and 2.1.2-4 in the Holos version 4.0 algorithm document. 

        Returns
        -------
            float: Above ground carbon input(kg N ha-1).
        """

        if self.group == "root":
            self.Above_Ground_Carbon_Input = self.c_s()
        else:
            self.Above_Ground_Carbon_Input = self.c_p_to_soil() + self.c_s()
        
        return self.Above_Ground_Carbon_Input


        
    def below_ground_carbon_input(self):
        """
        Calculates the below ground carbon input.
        Equation 2.1.2-3 and 2.1.2-5 in the Holos version 4.0 algorithm document. 

        Returns
        -------
            float: Below ground carbon input(kg N ha-1).
        """
        
        if self.group == "root":
            self.Below_Ground_Carbon_Input = self.c_p_to_soil() + self.c_e()
        else:
            self.Below_Ground_Carbon_Input = self.c_r() + self.c_e()
        
        return self.Below_Ground_Carbon_Input

    def get_crop_residue(self):
        """
        Get a dictionary containing crop residue results.

        Calculates and returns the following results:
        - 'C_p': plant carbon in agricultural product (kg ha-1).
        - 'above_ground_carbon_input': Aboveground residue carbon input (kg ha-1).
        - 'below_ground_carbon_input': Belowground residue carbon input (kg ha-1).
        - 'above_ground_residue_n': Nitrogen content of above-ground residue (kg N ha-1).
        - 'below_ground_residue_n': Nitrogen content of below-ground residue (kg N ha-1).
        - 'n_crop_residue': Nitrogen content of the crop residue (kg N).

        Returns
        -------
        dict: A dictionary containing the calculated crop residue.
        
        """
        
        all_data = {
            'C_p': self.c_p(),
            'above_ground_carbon_input': self.above_ground_carbon_input(),
            'below_ground_carbon_input': self.below_ground_carbon_input(),
            'above_ground_residue_n': self.above_ground_residue_n(),
            'below_ground_residue_n': self.below_ground_residue_n(),
            'n_crop_residue': self.n_crop_residue()
        }
        return all_data