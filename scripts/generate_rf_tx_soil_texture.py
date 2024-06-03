import os
import json

user_defined_rf_tx_distributions = {
    'midpoint': {
        'Clay (heavy)': 2.54,
        'Silty clay': 1.96,
        'Clay (light)': 1.77,
        'Silty clay loam': 1.52,
        'Clay loam': 1.38,
        'Silt': 1.09,
        'Silt loam': 1.15,
        'Sandy clay': 1.58,
        'Loam': 1.09,
        'Sandy clay loam': 1.13,
        'Sandy loam': 0.80,
        'Loamy sand': 0.61,
        'Sand': 0.53
    },
    
    'range': {
        'Clay (heavy)': (1.899, 2.920),
        'Silty clay': (1.642, 2.152),
        'Clay': (1.484, 2.152),
        'Silty clay loam': (1.392, 1.768),
        'Clay loam': (1.234, 1.642),
        'Silt': (0.874, 1.230),
        'Silt loam': (0.684, 1.518),
        'Sandy clay': (1.262, 1.772),
        'Loam': (0.806, 1.373),
        'Sandy clay loam': (0.879, 1.388),
        'Sandy loam': (0.495, 1.112),
        'Loamy sand': (0.369, 0.846),
        'Sand': (0.369, 0.687)
    }
}

# Get the directory of the current script
dir_path = os.path.dirname(os.path.realpath(__file__))
output_path = os.path.join(dir_path, '..', 'data', 'params_sampling_range', 'rf_tx_params_dist.json')
# Save to file
with open(output_path, 'w') as f:
    json.dump(user_defined_rf_tx_distributions, f, indent=4)
