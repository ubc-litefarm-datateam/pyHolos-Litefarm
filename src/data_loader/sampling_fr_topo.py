import numpy as np

def sampling_fr_topo(value, n, distribution='uniform'):
    low = value * 0.75
    high = value * 1.25
    results = []

    if distribution == 'uniform':
        results = np.random.uniform(low, high, n)
    elif distribution == 'normal':
        mean = value
        std_dev = (high - low) / 6  # Approx. 99.7% data within ±25%
        results = np.random.normal(mean, std_dev, n)
    elif distribution == 'lognormal':
        mean = np.log(value)
        std_dev = (np.log(high) - np.log(low)) / 6  # Scale to match range
        results = np.random.lognormal(mean, std_dev, n)
    else:
        raise ValueError("Unsupported distribution type.")

    return results

if __name__ == '__main__':
    value = 7.12
    n_samples = 5

    # Sampling using uniform distribution
    uniform_samples = sampling_fr_topo(value, n_samples, 'uniform')
    print("Uniform Distribution Samples:\n", uniform_samples)
    print(type(uniform_samples))

    # Sampling using normal distribution
    normal_samples = sampling_fr_topo(value, n_samples, 'normal')
    print("Normal Distribution Samples:\n", normal_samples)

    # Sampling using lognormal distribution
    lognormal_samples = sampling_fr_topo(value, n_samples, 'lognormal')
    print("Lognormal Distribution Samples:\n", lognormal_samples)
