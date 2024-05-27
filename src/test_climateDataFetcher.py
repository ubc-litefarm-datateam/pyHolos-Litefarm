from data_loader.get_external_climate_params import ExternalClimateDataFetcher

if __name__ == '__main__':
    points = [(-93.6250, 42.0329), (-89.3985, 43.0731)]  # Example list of points
    start_year = 2017
    end_year = 2021
    fetcher = ExternalClimateDataFetcher(points, start_year, end_year)
    averages = fetcher.process_points_over_years()
    print("Averages:", averages)


# [
#     {"success": True, "data": {"P": 100, "PE": 25}, "point": (-93.6250, 42.0329), "year": 2019},
#     {"success": True, "data": {"P": 110, "PE": 30}, "point": (-93.6250, 42.0329), "year": 2020},
#     {"success": False, "error": "Timeout error", "point": (-93.6250, 42.0329), "year": 2021},
#     {"success": True, "data": {"P": 95, "PE": 20}, "point": (-89.3985, 43.0731), "year": 2019},
#     {"success": True, "data": {"P": 105, "PE": 22}, "point": (-89.3985, 43.0731), "year": 2020},
#     {"success": True, "data": {"P": 100, "PE": 23}, "point": (-89.3985, 43.0731), "year": 2021}
# ]

# {
#     "(-93.6250, 42.0329)": {
#         "success": true,
#         "data": {
#             "P": 120.5,
#             "PE": 30.7
#         }
#     },
#     "(-89.3985, 43.0731)": {
#         "success": true,
#         "data": {
#             "P": 110.0,
#             "PE": 25.3
#         }
#     },
    # "(-88.0430, 41.8798)": {
    #     "success": false,
    #     "error": "Timeout error during data fetching"
    # },
#     "(-90.6485, 42.9981)": {
#         "success": true,
#         "data": {
#             "P": 105.2,
#             "PE": 28.1
#         }
#     },
    # "(-92.3814, 43.0261)": {
    #     "success": false,
    #     "error": "Incomplete data for the growing season."
    # }
# }