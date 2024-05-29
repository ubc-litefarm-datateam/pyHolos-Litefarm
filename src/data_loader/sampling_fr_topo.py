import numpy as np

def sampling_fr_topo(value, n, distribution='uniform'):
    low = value * 0.75
    high = value * 1.25
    results = []

    if distribution == 'uniform':
        results = np.random.uniform(low, high, (n, 10))
    elif distribution == 'normal':
        mean = value
        std_dev = (high - low) / 6  # Approx. 99.7% data within ±25%
        results = np.random.normal(mean, std_dev, (n, 10))
    elif distribution == 'lognormal':
        mean = np.log(value)
        std_dev = (np.log(high) - np.log(low)) / 6  # Scale to match range
        results = np.random.lognormal(mean, std_dev, (n, 10))
    else:
        raise ValueError("Unsupported distribution type.")

    return results