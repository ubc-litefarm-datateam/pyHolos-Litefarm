from data_loader.get_external_soil_params import ExternalSoilTextureDataFetcher

points = [(-88.86, 54.39), (-89.00, 54.50)]  # List of (lon, lat) tuples
fetcher = ExternalSoilTextureDataFetcher(points)
texture_mapped_values = fetcher.process()
print(texture_mapped_values)