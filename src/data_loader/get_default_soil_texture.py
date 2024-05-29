import os
import pandas as pd

class ModifierSoilTexture:
    """
    Holos RF_TX values: fetches soil texture based on the region from 
    parameters provided by Holos.
    """
    def __init__(self, farm_data, soil_texture='unknown'):
        self.farm_data = farm_data
        self.province = farm_data['province']
        self.soil_texture = soil_texture
        self.dir = os.path.dirname(__file__)
        self.soil_texture_path = os.path.join(self.dir, f'../../data/preprocessed/modifier_rf_tx.csv')
        self.rf_tx = self.get_rf_tx_modifier()

    def get_rf_tx_modifier(self):
        region = self.get_region()
        soil_texture_df = pd.read_csv(self.soil_texture_path)
        rf_tx = soil_texture_df.query(f"region == '{region}' & soil_texture == '{self.soil_texture}'")['value'].iloc[0]
        return rf_tx
    
    def get_region(self):
        western_canada = ['Alberta', 'British Columbia', 
                          'Manitoba', 'Saskatchewan', 
                          'Northwest Territories', 'Nunavut']
        
        return 'western_canada' if self.province in western_canada else 'eastern_canada'


if __name__ == '__main__':
    # Example farm data
    farm_data = {
        'province': 'Quebec',  # Province should be one that is recognized by your class
    }
    # Example soil texture
    soil_texture = 'fine'  # Soil texture should be one that is available in your CSV file

    # Initialize the ModifierSoilTexture class with the example farm data and soil texture
    modifier = ModifierSoilTexture(farm_data, soil_texture)

    # Fetch and print the RF_TX modifier
    rf_tx_modifier = modifier.get_rf_tx_modifier()
    print(f"RF_TX Modifier for the region and soil texture: {rf_tx_modifier}")
