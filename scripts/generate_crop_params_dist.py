"""
This script allows users to define distributions for various parameters associated with crops.
Customize the 'user_defined_crop_params_distributions' dictionary to tailor it to specific crops
with your chosen distribution types and parameters.

The defined distributions are automatically saved as a JSON file in the 'data/params_sampling_range' 
directory. The output path is pre-configured for consistency and should not be modified.
"""

import json
import os

user_defined_crop_params_distributions = {
    "Wheat": {
        "moisture": ("uniform", 10, 14),  # Adjusted to your desired range
        "R_p": ("normal", 0.219, 0.02),
        "R_s": ("lognormal", -0.597, 0.1), # Log of mean and std dev
        "R_r": ("uniform", 0.1, 0.17),
        "R_e": ("normal", 0.095, 0.01),
        "N_p": ("normal", 27.9, 2),
        "N_s": ("uniform", 6, 11),
        "N_r": ("uniform", 10, 15),
        "N_e": ("normal", 13.4, 1),
    },
    "Oats": {
        "moisture": ("uniform", 11, 13), 
        "R_p": ("normal", 0.319, 0.032),
        "R_s": ("lognormal", -1.262, 0.056),  
        "R_r": ("uniform", 0.2, 0.28),
        "R_e": ("normal", 0.157, 0.016),
        "N_p": ("normal", 18.0, 1.8),
        "N_s": ("uniform", 5, 7),
        "N_r": ("uniform", 9, 11),
        "N_e": ("normal", 10.0, 1.0),
    },
}

# Get the directory of the current script
dir_path = os.path.dirname(os.path.realpath(__file__))
output_path = os.path.join(
    dir_path, "..", "data", "params_sampling_range", "crop_params_dist.json"
)
# Save to file
with open(output_path, "w") as f:
    json.dump(user_defined_crop_params_distributions, f, indent=4)
