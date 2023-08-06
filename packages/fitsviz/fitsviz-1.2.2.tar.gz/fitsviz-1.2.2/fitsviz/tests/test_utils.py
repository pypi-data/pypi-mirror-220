import pytest
import numpy as np

from fitsviz.utils.cutils import load_fits, sci_to_rms, get_image_with_least_freq, calculate_spectral_indices


# Test load_fits function
def test_load_fits():
    data = load_fits( "VLASS1.2.se.T01t08.J033228-363000.06.2048.v1.spw2.I.iter3.image.pbcor.tt0.subim.fits")
    assert isinstance(data, np.ndarray)
    assert data.ndim == 2

# Test sci_to_rms function
def test_sci_to_rms():
    rms_data = sci_to_rms("path/to/science_file.fits")
    assert isinstance(rms_data, np.ndarray)
    assert rms_data.ndim == 2



# Test get_image_with_least_freq function
def test_get_image_with_least_freq():
    img_names = ["VLASS1.2.se.T01t08.J033228-363000.06.2048.v1.spw3.I.iter3.image.pbcor.tt0.subim.fits", "VLASS1.2.se.T01t08.J033228-363000.06.2048.v1.spw6.I.iter3.image.pbcor.tt0.subim.fits", "VLASS1.2.se.T01t08.J033228-363000.06.2048.v1.spw2.I.iter3.image.pbcor.tt0.subim.fits"]
    least_freq_img = get_image_with_least_freq(img_names)
    assert least_freq_img == img_names[-1]

