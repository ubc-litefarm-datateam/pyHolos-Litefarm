import os
import rasterio
import pandas as pd

class ExternalSoilTextureDataFetcher:
    def __init__(self, points):
        self.points = points
        self.dir = os.path.dirname(__file__)
        self.smu_csv_path = os.path.join(self.dir, 
                                         '../data/external/HWSD2/HWSD2_SMU.csv') 
        self.texture_csv_path = os.path.join(self.dir, 
                                             '../data/external/HWSD2/D_TEXTURE_USDA.csv')
        self.texture_mapped_path = os.path.join(self.dir,
                                                '../data/preprocessed/soil_texture_mapped_values.csv')
        self.raster_path = os.path.join(self.dir,
                                        '../data/external/HWSD2_RASTER/HWSD2.bil')
        self.src = None
        self.load_data()

    def load_data(self):
        self.smu_df = pd.read_csv(self.smu_csv_path)
        self.texture_df = pd.read_csv(self.texture_csv_path)
        self.mapped_value_df = pd.read_csv(self.texture_mapped_path)

    def open_raster(self):
        self.src = rasterio.open(self.raster_path)

    def close_raster(self):
        if self.src:
            self.src.close()

    def get_raster_value(self, lon, lat):
        row, col = self.src.index(lon, lat)
        return self.src.read(1)[row, col]

    def lookup_texture_and_value(self, smu_id):
        texture_code = self.smu_df[self.smu_df['HWSD2_SMU_ID'] == smu_id]['TEXTURE_USDA'].iloc[0]
        texture_type = self.texture_df[self.texture_df['CODE'] == texture_code]['VALUE'].iloc[0]
        texture_mapped_value = self.mapped_value_df[self.mapped_value_df['VALUE'] == texture_type]['AWC'].iloc[0]

        return texture_mapped_value

    def process(self):
        self.open_raster()
        smu_ids = [self.get_raster_value(lon, lat) for lon, lat in self.points]
        self.close_raster()
        texture_mapped_values = [self.lookup_texture_and_value(smu_id) for smu_id in smu_ids]
        return texture_mapped_values


