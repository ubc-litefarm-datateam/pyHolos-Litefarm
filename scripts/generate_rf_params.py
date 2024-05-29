import json
import os
# Define user distributions matching all parameters for clarity
user_defined_rf_params_distributions = {
    'RF_AM': ('uniform', 0.9, 1.1),
    'RF_CS': ('uniform', 0.9, 1.1),
    'RF_NS': ('normal', 0.84, 0.02),
    'RF_Till': ('lognormal', -0.10536, 0.1)
}

# Get the directory of the current script
dir_path = os.path.dirname(os.path.realpath(__file__))
output_path = os.path.join(dir_path, '..', 'data', 'params_sampling_range', 'rf_params_dist.json')
# Save to file
with open(output_path, 'w') as f:
    json.dump(user_defined_rf_params_distributions, f, indent=4)
