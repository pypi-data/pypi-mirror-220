"""
This module implements the ApertureDAO class,utilizing the DAOStarFinder algorithm 
Link: https://ui.adsabs.harvard.edu/abs/1987PASP...99..191S/abstract
"""

from fitsviz.utils import cutils as cu
import dask
import sys
import logging
from astropy.io import fits
from photutils.detection import DAOStarFinder
from astropy.stats import sigma_clipped_stats
from functools import cached_property
from fitsviz.detection.core import DetectionBase
import pandas as pd
import numpy as np
import dask.dataframe as dd
import multiprocessing


class ApertureDAO(DetectionBase):
    """_summary_

    Args:
        DetectionBase : Base class for source detection
    """

    def __init__(self, science_images):

        # names of the science images
        self.science_images = science_images

    @cached_property
    def science_images(self):
        return self.science_images

    @cached_property
    def freqs(self):
        return [fits.getheader(sci)["CRVAL3"] for sci in self.science_images]

    def get_sources(self, science_data, rms_data):
        """Given science and rms files, apply the DAOStarFinder
        source detection algorithm to get summary statistics
        on those files.

        Args:
            science_data (np.ndarray): Science data
            rms_data (np.ndarray): RMS data

        Returns:
            sources,summary (np.ndarray,list): List of sources and summary statistics
        """

        try:

            # Sigma clipped statistics for RMS file
            mean, median, _ = sigma_clipped_stats(rms_data, sigma=3.0)
            # find the stars with DAO alg


            daofind = DAOStarFinder(fwhm=3.0, threshold=5. * mean)
            
            sources = daofind(science_data - median)
        except:
            logging.exception(msg = "No sources found")
            sys.exit()
        
        return sources

    @dask.delayed
    def _calculate_flux(self, sci, positions):
        sciimg = cu.load_fits(sci)
        median = np.nanmedian(cu.sci_to_rms(sci))
        flux_accross_frequencies = []
        # Median subtraction
        adj_sci = sciimg - median
        # Go through every source and find its flux
        for _, row in positions.iterrows():
            x = int(row[0])
            y = int(row[1])
            # Flux is crudely defined as the sum of values inside the aperture
            flux = np.nansum(adj_sci[y - 5: y + 5, x - 5: x + 5])
            flux_accross_frequencies.append(flux)
        return flux_accross_frequencies

    def get_fluxs(self, sources):
        """
        Given a list of sources, get mean flux and spectral index

        Args:
            sources (astropy.table.QTable):

        Returns:
            summary (pd.DataFrame): Summary statistics
        """

        # Convert QTable to Dask DataFrame and select centroids
        positions = dd.from_pandas(sources["xcentroid", "ycentroid"].to_pandas(
        ), npartitions=multiprocessing.cpu_count())
        self.positions = positions
        # Initialize an empty Dask DataFrame
        flux_df = dd.from_pandas(
            pd.DataFrame(), npartitions=multiprocessing.cpu_count())
        # Calculate flux for each science image

        fluxes = [self._calculate_flux(sci, positions)
                  for sci in self.science_images]
        fluxes = dask.compute(*fluxes)

        for flux in fluxes:
            flux_df = flux_df.append(pd.Series(flux))

        # Get frequencies of all files, transpose for row processing
        flux_df = flux_df.compute()
        flux_df = flux_df.T

        flux_df.columns = self.freqs

        # spectral index list
        return flux_df

    def get_summary(self, flux_df):
        """
        Given a dataframe of flux values, calculate the spectral index
        and return a dataframe with source positions , flux at lowest frequency
        and spectral index

        Args:
            flux_df (_type_): _description_

        Returns:
            _type_: _description_
        """
        spx = [cu.calculate_spectral_indices(
            self.freqs, row) for _, row in flux_df.iterrows()]

        # set file names
        # lowest frequency image fluxes
        lowest_source_col = np.min(self.freqs)
        summary = self.positions.join(flux_df[[lowest_source_col]])

        # Rows: x coordinate, y coordinate, flux of lowest frequency, spectral index of source
        summary = summary.rename(columns={lowest_source_col: "flux"}).compute()
        summary["spectral_index"] = spx
        summary.fillna(0)
        return summary
