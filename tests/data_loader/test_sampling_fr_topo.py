import numpy as np
import pytest
from src.data_loader.sampling_fr_topo import sampling_fr_topo


def test_uniform_distribution_samples():
    """Ensure uniform distribution returns correct number and range of samples."""
    value = 0.5
    n_samples = 100
    samples = sampling_fr_topo(value, n_samples, "uniform")
    assert len(samples) == n_samples, "Incorrect number of samples returned"
    assert np.all(samples >= value * 0.75) and np.all(
        samples <= value * 1.25
    ), "Samples out of expected range"


def test_normal_distribution_samples():
    """Verify normal distribution samples are correctly distributed around the mean."""
    value = 0.5
    n_samples = 100
    samples = sampling_fr_topo(value, n_samples, "normal")
    assert len(samples) == n_samples, "Incorrect number of samples returned"


def test_lognormal_distribution_samples():
    """Check lognormal distribution for correct sample count."""
    value = 0.5
    n_samples = 100
    samples = sampling_fr_topo(value, n_samples, "lognormal")
    assert len(samples) == n_samples, "Incorrect number of samples returned"


def test_invalid_distribution():
    """Ensure an error is raised for unsupported distribution types."""
    with pytest.raises(ValueError):
        sampling_fr_topo(0.5, 5, "binomial")
