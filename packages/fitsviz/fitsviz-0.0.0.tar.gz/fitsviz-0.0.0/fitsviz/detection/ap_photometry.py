"""
This module implements the ApertureDAO class,utilizing the DAOStarFinder algorithm 
"""

from fitsviz.utils import cutils as cu
import time
import dask
from astropy.io import fits
from photutils.detection import DAOStarFinder
from astropy.stats import sigma_clipped_stats
from fitsviz.detection.core import DetectionBase
import pandas as pd
import numpy as np
from numba import jit
import concurrent.futures
import dask.dataframe as dd
from dask.distributed import Client
import multiprocessing


class ApertureDAO(DetectionBase):
    """
    Args:
        DetectionBase (_type_): _description_

    Returns:
        _type_: _description_
    """

    def __init__(self):
        pass



    # def process_sources(self, sources, sci_img_list):
    #     """
    #     Given a list of sources,get mean flux and spectral index

    #     Args:
    #         sources (pd.DataFrame):

    #     Returns:
    #         _type_: _description_
    #     """

    #     # Convert QTable to pandas and select centroids
    #     positions = sources["xcentroid", "ycentroid"].to_pandas()
    #     # print(positions)
    #     # Initialize pandas dataframe with source numbers as columns
    #     flux_df = pd.DataFrame(columns=positions.index)

    #     for sci in sci_img_list:

    #         sciimg = cu.load_fits(sci)

    #         median = np.nanmedian(cu.sci_to_rms(sci))

    #         flux_accross_frequencies = []
    #         # median subtraction
    #         adj_sci = sciimg - median

    #         # go through every source and find its flux
    #         for _, row in positions.iterrows():

    #             x = int(row[0])
    #             y = int(row[1])
    #             # flux is crudely defined as sum of values inside aperture
    #             flux = np.nansum(adj_sci[y - 5: y + 5, x - 5: x + 5])

    #             flux_accross_frequencies.append(flux)


    #         flux_df.loc[len(flux_df)] = flux_accross_frequencies

    #     # get frequencies of all files
    #     freqs = [fits.getheader(sci)['CRVAL3'] for sci in sci_img_list]
    #     # transpose flux dataframe and iterate accross rows
    #     flux_df = flux_df.T
    #     # calculate spectral index of each source
    #     flux_df["spectral_index"] = [
    #         cu.calculate_spectral_indices(freqs, row) for _, row in flux_df.iterrows()
    #     ]
    #     # rows: x coordinate, y coordinate,flux of lowest frequency,spectral
    #     # index of source
    #     lowest_idx = np.argmin(freqs)
    #     summary = positions.join(flux_df[[lowest_idx, "spectral_index"]])
    #     summary = summary.rename(columns={lowest_idx: "flux"})

    #     return summary
    
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
        st = time.time()
        mean, median, _ = sigma_clipped_stats(rms_data, sigma=3.0)
        end = time.time()

        st2 = time.time()
        daofind = DAOStarFinder(fwhm=3.0, threshold=5. * mean)

        sources = daofind(science_data - median)
        end2 = time.time()

        return sources
    

    @dask.delayed
    def calculate_flux(self,sci,positions):
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
            flux = np.nansum(adj_sci[y - 5 : y + 5, x - 5 : x + 5])
            flux_accross_frequencies.append(flux)
        return flux_accross_frequencies

    # # DASK INITIAL ATTEMPT
    def process_sources(self, sources, sci_img_list):
        """
        Given a list of sources, get mean flux and spectral index

        Args:
            sources (pd.DataFrame):

        Returns:
            summary (pd.DataFrame): Summary statistics
        """
        client = Client()

        # Convert QTable to Dask DataFrame and select centroids
        positions = dd.from_pandas(sources["xcentroid", "ycentroid"].to_pandas(), npartitions=multiprocessing.cpu_count())

        # Initialize an empty Dask DataFrame
        flux_df = dd.from_pandas(pd.DataFrame(), npartitions=multiprocessing.cpu_count())
        # Calculate flux for each science image
        fluxes = [self.calculate_flux(sci,positions) for sci in sci_img_list]
        fluxes = dask.compute(*fluxes)

        for flux in fluxes:
            flux_df = flux_df.append(pd.Series(flux))
        
        # Get frequencies of all files
        freqs = [fits.getheader(sci)["CRVAL3"] for sci in sci_img_list]
        flux_df = flux_df.compute()
        flux_df = flux_df.T


        spx = [cu.calculate_spectral_indices(freqs, row) for _, row in flux_df.iterrows()]
        flux_df.columns = [i for i in range(len(flux_df.columns))]
        flux_df["spectral_index"] = spx
        # Rows: x coordinate, y coordinate, flux of lowest frequency, spectral index of source
        lowest_idx = np.argmin(freqs)
        summary = positions.join(flux_df[[lowest_idx, "spectral_index"]])
        summary = summary.rename(columns={lowest_idx: "flux"}).compute()

        

        client.close()

        return summary


    # def process_sources(self, sources, sci_img_list):
    #     """
    #     Given a list of sources, get mean flux and spectral index

    #     Args:
    #         sources (pd.DataFrame):

    #     Returns:
    #         summary (pd.DataFrame): Summary statistics
    #     """
    #     # Initialize Dask client
    #     client = Client()

    #     # Convert QTable to Dask DataFrame and select centroids
    #     positions = sources[["xcentroid", "ycentroid"]].to_pandas()

    #     # Initialize an empty Dask DataFrame
    #     flux_df = dd.from_pandas(pd.DataFrame(), npartitions=1)

    #     @dask.delayed
    #     def calculate_flux(sci):
    #         sciimg = cu.load_fits(sci)
    #         median = np.nanmedian(cu.sci_to_rms(sci))
    #         flux_accross_frequencies = []

    #         # Median subtraction
    #         adj_sci = sciimg - median

    #         for index,row in positions.iterrows():
    #             x = int(row[0])
    #             y=int(row[1])
    #             # Flux is crudely defined as the sum of values inside the aperture
    #             flux = np.nansum(adj_sci[y - 5 : y + 5, x - 5 : x + 5])
    #             flux_accross_frequencies.append(flux)

    #         return flux_accross_frequencies

    #     # Calculate flux for each science image
    #     fluxes = [calculate_flux(sci) for sci in sci_img_list]
    #     fluxes = dask.compute(*fluxes)

    #     for flux in fluxes:
    #         flux_df = flux_df.assign(**{f"flux_{i}": pd.Series(flux[i]) for i in range(len(flux))})

    #     # Get frequencies of all files
    #     freqs = [fits.getheader(sci)["CRVAL3"] for sci in sci_img_list]

    #     # Calculate spectral index of each source
    #     @dask.delayed
    #     def calculate_spectral_index(row):
    #         return cu.calculate_spectral_indices(freqs, row)

    #     flux_df["spectral_index"] = flux_df.apply(
    #         calculate_spectral_index, axis=1, meta=("spectral_index", "float64")
    #     ).compute()

    #     # Rows: x coordinate, y coordinate, flux of lowest frequency, spectral index of source
    #     lowest_idx = np.argmin(freqs)
    #     summary = sources.join(flux_df[[f"flux_{lowest_idx}", "spectral_index"]])
    #     summary = summary.rename(columns={f"flux_{lowest_idx}": "flux"})

    #     # Close the Dask client
    #     client.close()

    #     return summary


    