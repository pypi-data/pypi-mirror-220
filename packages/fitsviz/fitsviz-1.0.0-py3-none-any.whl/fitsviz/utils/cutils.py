"""
Common utils for all modules and algorithms
"""
from astropy.io import fits
import numpy as np
from dask.distributed import Client


def load_fits(file_name):
    """
    Load FITS files and index into data

    Args:
        file_name (str):file path 

    Returns:
        np.ndarray: Returned fits file at the first axis
    """
    return fits.getdata(file_name)[0, 0, :, :]


def sci_to_rms(file_name):
    """
    Given a science filename, load its corresponding 

    Args:
        file_name (str):file path 

    Returns:
        np.ndarray: Returned fits file at the first axis
    """
    file_name = file_name.replace("tt0.subim.fits", "tt0.rms.subim.fits")
    return fits.getdata(file_name)[0, 0, :, :]


def get_image_with_least_freq(science_img_names):
    """
    Given a list of science files, get the image name with the lowest frequency.
    Args:
        science_img_names (list[str]): science file names

    Returns:
        str: science file name of lowest frequency
    """
    # maximum value for a 64-bit signed integer.
    cur_freq = 9223372036854775807
    least_freq_img = None

    for sci_img in science_img_names:
        sci_img_freq = fits.getheader(sci_img)['CRVAL3']
        if cur_freq > sci_img_freq:
            cur_freq = sci_img_freq
            least_freq_img = sci_img
    return least_freq_img


def create_dask_client(n_workers=4):
    """Clean up dask dask client on system exit

    Args:
        dask_client (dask.distributed.Client): Dask client
    """
    client = Client(n_workers=n_workers)
    return client


def calculate_spectral_indices(frequencies, flux_densities):
    """
    Calculate the spectral index of a source given a list of frequencies and flux densities
    Args:
        frequencies (list[float]): List of frequencies
        flux_densities (list[float]): List of flux densities
        Returns:
            spectral_index (float): Spectral index of the source
    """
    log_frequencies = np.log10(frequencies)
    log_flux_densities = np.log10(flux_densities)

    # Fit a linear regression to calculate the spectral index
    coefficients = np.polyfit(log_frequencies, log_flux_densities, deg=1)
    spectral_index = coefficients[0]

    return spectral_index


def cleanup_dask_client(dask_client):
    """Clean up dask dask client on system exit

    Args:
        dask_client (dask.distributed.Client): Dask client
    """
    if dask_client is not None:
        dask_client.close()
