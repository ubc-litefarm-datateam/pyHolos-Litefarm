import os
import pandas as pd
import geopandas as gpd

class Modifiers:
    def __init__(self, farm_data, soil_texture='unknown'):
        self.farm_data = farm_data
        self.soil_texture = soil_texture
        self.dir = os.path.dirname(__file__)
        self.modifiers = self.get_modifiers()

    def get_modifiers(self, rf_am='default', rf_cs='Annual', rf_ns='RF_NS_CRN', tillage='unknown', soil_texture='unknown'):
        region = self.get_region()
        modifiers = {}
        # Define the list of modifiers and the relevant files
        modifier_files = {
            'RF_AM': 'modifier_rf_am.csv',
            'RF_CS': 'modifier_rf_cs.csv',
            'RF_NS': 'modifier_rf_ns.csv',
            'RF_Till': 'modifier_rf_till.csv',
            'RF_TX': 'modifier_rf_tx.csv'
        }

        # Iterate over the modifier files, loading and querying as needed
        for key, filename in modifier_files.items():
            path = os.path.join(self.dir, f'../../data/preprocessed/{filename}')
            df = pd.read_csv(path)
            
            if key == 'RF_AM':
                value = df.query(f"method == '{rf_am}'")['value'].iloc[0]
            elif key == 'RF_CS':
                value = df.query(f"group == '{rf_cs}'")['value'].iloc[0]
            elif key == 'RF_NS':
                value = df.query(f"N_source == '{rf_ns}'")['value'].iloc[0]
            elif key == 'RF_Till':
                value = df.query(f"region == '{region}' & tillage == '{tillage}'")['value'].iloc[0]
            elif key == 'RF_TX':
                value = df.query(f"region == '{region}' & soil_texture == '{self.soil_texture}'")['value'].iloc[0]

            modifiers[key] = value

        return modifiers

    def get_region(self):
        province = self.farm_data.province
        western_canada = ['Alberta', 'British Columbia', 
                          'Manitoba', 'Saskatchewan', 
                          'Northwest Territories', 'Nunavut']
        
        return 'western_canada' if province in western_canada else 'eastern_canada'
        