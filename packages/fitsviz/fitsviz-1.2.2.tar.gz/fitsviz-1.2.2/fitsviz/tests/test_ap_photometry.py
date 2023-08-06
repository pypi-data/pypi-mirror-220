import pytest
import numpy as np
from astropy.io import fits
from dask.distributed import Client
from fitsviz.detection.ap_photometry import ApertureDAO
import pandas as pd

# Test the ApertureDAO class

def test_get_sources():
    # Create test science and rms data
    science_data = np.random.rand(100, 100)
    rms_data = np.random.rand(100, 100)

    # Instantiate ApertureDAO
    dao = ApertureDAO(["sci1.fits", "sci2.fits"])

    # Call the get_sources method
    sources = dao.get_sources(science_data, rms_data)

    # Assert the output type and shape
    assert isinstance(sources, np.ndarray)
    assert sources.ndim == 2

def test_calculate_flux():
    # Create test positions DataFrame
    positions = pd.DataFrame({'x': [10, 20], 'y': [15, 25]})

    # Instantiate ApertureDAO
    dao = ApertureDAO(["sci1.fits", "sci2.fits"])

    # Call the calculate_flux method
    flux = dao.calculate_flux("sci1.fits", positions)

    # Assert the output type and shape
    assert isinstance(flux, list)
    assert len(flux) == 2

def test_get_fluxs():
    # Create test sources DataFrame
    sources = pd.DataFrame({'xcentroid': [10, 20], 'ycentroid': [15, 25]})

    # Instantiate ApertureDAO
    dao = ApertureDAO(["sci1.fits", "sci2.fits"])

    # Call the get_fluxs method
    flux_df = dao.get_fluxs(sources)

    # Assert the output type and shape
    assert isinstance(flux_df, pd.DataFrame)
    assert flux_df.shape == (2, 2)

def test_get_summary():
    # Create test flux_df DataFrame
    flux_df = pd.DataFrame({'10': [0.1, 0.2], '20': [0.3, 0.4]})

    # Instantiate ApertureDAO
    dao = ApertureDAO(["sci1.fits", "sci2.fits"])

    # Call the get_summary method
    summary = dao.get_summary(flux_df)

    # Assert the output type and shape
    assert isinstance(summary, pd.DataFrame)
    assert summary.shape == (2, 4)

# Add more tests as needed


