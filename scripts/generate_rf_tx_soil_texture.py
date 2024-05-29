import os
import json

user_defined_rf_tx_distributions = {
    'midpoint': {
        'Clay (heavy)': 2.5455543408506496,
        'Silty clay': 1.9560194010574545,
        'Clay (light)': 1.705779710928461,
        'Silty clay loam': 1.4536697205144404,
        'Clay loam': 1.3282382782822517,
        'Silt': 1.1097535862760832,
        'Silt loam': 1.171897631095388,
        'Sandy clay': 1.5935354012770122,
        'Loam': 1.03079272168764,
        'Sandy clay loam': 1.1277176835933889,
        'Sandy loam': 0.7780629551974809,
        'Loamy sand': 0.7008017800969404,
        'Sand': 0.5498953463873104
    },
    
    'range': {
        'Clay (heavy)': (1.8586863753799996, 2.832422306321299),
        'Silty clay': (1.6125854183221298, 2.0994533837927793),
        'Clay': (1.4621060380641424, 2.0994533837927793),
        'Silty clay loam': (1.374370518500361, 1.7329689225285199),
        'Clay loam': (1.2238911382423736, 1.6125854183221298),
        'Silt': (0.8796164957936101, 1.2198906767585558),
        'Silt loam': (0.6990412394840253, 1.4947540227067508),
        'Sandy clay': (1.2501014185416874, 1.7369693840123375),
        'Loam': (0.8152724505058772, 1.3563129928694024),
        'Sandy clay loam': (0.8849504444387004, 1.3704849227480773),
        'Sandy loam': (0.5184659831744405, 1.1076599272205216),
        'Loamy sand': (0.39808247896805055, 0.8535210812258303),
        'Sand': (0.39808247896805055, 0.7017082138065704)
    }
}

# Get the directory of the current script
dir_path = os.path.dirname(os.path.realpath(__file__))
output_path = os.path.join(dir_path, '..', 'data', 'params_sampling_range', 'rf_tx_params_dist.json')
# Save to file
with open(output_path, 'w') as f:
    json.dump(user_defined_rf_tx_distributions, f, indent=4)
