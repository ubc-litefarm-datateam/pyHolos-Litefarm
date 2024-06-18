"""
This script allows users to define distributions for various parameters associated with crop groups.
Customize the 'user_defined_crop_group_params_distributions' dictionary to tailor it to specific crops
with your chosen distribution types and parameters.

The defined distributions are automatically saved as a JSON file in the 'data/params_sampling_range' directory. 
The output path is pre-configured for consistency and should not be modified.
"""

import json
import os

user_defined_crop_group_params_distributions = {
    "Annual": {
        "carbon_concentration": ("uniform", 0.4, 0.5),
        "S_s": ("normal", 100, 10),
        "S_r": ("lognormal", 4.6, 0.1),  # Log of mean and std deviation
        "S_p": ("uniform", 1.5, 2.5),
    }
    # Additional crops can be added similarly
}

# Get the directory of the current script
dir_path = os.path.dirname(os.path.realpath(__file__))
output_path = os.path.join(
    dir_path, "..", "data", "params_sampling_range", "crop_group_params_dist.json"
)
# Save to file
with open(output_path, "w") as f:
    json.dump(user_defined_crop_group_params_distributions, f, indent=4)
