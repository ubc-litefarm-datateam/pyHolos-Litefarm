import numpy as np


def sampling_fr_topo(value, n, distribution="uniform"):
    """
    Generates a sample of 'n' values from a specified statistical distribution
    based on a given FR_topo value (i.e., the fraction of land occupied by the
    lower portions of the landscape.

    This function allows sampling from 'uniform', 'normal', or 'lognormal' distributions.

    Parameters
    ----------
    value : float
        The fraction of land (FR_topo) occupied by lower portions of the landscape.
        This value is used as the central measure to define the range or parameters
        of the chosen distribution.
    n : int
        The number of samples to generate.
    distribution : str, optional
        The type of distribution to sample from. Supported values are 'uniform', 'normal',
        and 'lognormal'. The default is 'uniform'.

    Returns
    -------
    np.ndarray
        An array of sampled values.

    Raises
    ------
    ValueError
        If an unsupported distribution type is specified.

    Examples
    --------
    >>> sampling_fr_topo(0.5, 5, 'uniform')
    array([0.375, 0.468, 0.549, 0.421, 0.498])

    >>> sampling_fr_topo(0.5, 3, 'normal')
    array([0.521, 0.489, 0.502])

    >>> sampling_fr_topo(0.5, 2, 'lognormal')
    array([0.512, 0.488])
    """
    low = value * 0.75
    high = value * 1.25
    results = []

    if distribution == "uniform":
        results = np.random.uniform(low, high, n)
    elif distribution == "normal":
        mean = value
        std_dev = (high - low) / 6  # Approx. 99.7% data within ±25%
        results = np.random.normal(mean, std_dev, n)
    elif distribution == "lognormal":
        mean = np.log(value)
        std_dev = (np.log(high) - np.log(low)) / 6  # Scale to match range
        results = np.random.lognormal(mean, std_dev, n)
    else:
        raise ValueError("Unsupported distribution type.")

    return results


if __name__ == "__main__":
    test_value = 7.12
    test_n_samples = 5

    # Sampling using uniform distribution
    uniform_samples = sampling_fr_topo(test_value, test_n_samples, "uniform")
    print("Uniform Distribution Samples:\n", uniform_samples)

    # Sampling using normal distribution
    normal_samples = sampling_fr_topo(test_value, test_n_samples, "normal")
    print("Normal Distribution Samples:\n", normal_samples)

    # Sampling using lognormal distribution
    lognormal_samples = sampling_fr_topo(test_value, test_n_samples, "lognormal")
    print("Lognormal Distribution Samples:\n", lognormal_samples)
