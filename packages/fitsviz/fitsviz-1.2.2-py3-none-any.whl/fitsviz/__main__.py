""" 
__main__.py for supporting command line utility

"""
from fitsviz.utils import cutils as cu
from fitsviz.detection.ap_photometry import ApertureDAO
import click
import glob
import os
from os import path
import logging
from dask.distributed import Client
import json
import pandas as pd
from fitsviz.viz import plot_bokeh


logging.basicConfig(level=logging.INFO)


@click.group()
def fitsviz():
    """fitsviz: Autodetection of sources and visualization of FITS files"""


@fitsviz.command()
@click.option('link_file',
              '-i',
              type=click.Path(exists=True), required=True, help="path to link.json")
@click.option('vis_type', '-vt', '--vis_type', required=True,
              type=click.Choice(['raw', 'grid', 'fvf']), help='raw = Large science image with highlighted sources\n,grid = show interactive gridded plot of sources,\n fvf = plot flux vs frequency of all sources\n')
@click.option('output_dir',
              '-od',
              type=click.Path(exists=True),
              default=os.getcwd(), help='OPTIONAL, Output directory ,Defaults to pwd')
@click.option('backend', '-b', '--backend', default='bokeh',
              type=click.Choice(['bokeh']), help='OPTIONAL: Visualization backend, Defaults to Bokeh')
def mkviz(link_file, output_dir, backend, vis_type):
    """visualize the lowest frequency science image in a directory"""

    # Load link file
    with open(link_file, "r") as json_file:
        data = json.load(json_file)

    # Getting link file attributes
    sci_file = data["science_file"]
    flux_df = pd.read_csv(data["flux_freq_file"])
    sources = pd.read_csv(data["summary_file"])
    if backend == "bokeh":
        if vis_type == "all":
            plot_bokeh.plot_flux_freq(flux_df, sources)
        elif vis_type == "grid":
            plot_bokeh.grid_view(sci_file, sources)
        elif vis_type == "fvf":
            plot_bokeh.visualize_source(sci_file, sources)


@fitsviz.command()
@click.option('input_dir',
              '-i',
              type=click.Path(exists=True), required=True, help='Directory containig all science and RMS images, Defaults to pwd')
@click.option('output_dir',
              '-od',
              type=click.Path(exists=True),
              default='.', help='OPTIONAL, Defaults to pwd')
@click.option('output_file_name', '-o', '--output_file_name',
              default='sources.csv', help='OPTIONAL,defaults to sources.csv')
@click.option("algorithm",
              "-a",
              "--algorithm",
              default="aperture",
              type=click.Choice(["aperture"]),
              help="OPTIONAL, source detection algorithm, Defaults to aperture")
def mkstat(input_dir, output_dir, output_file_name, algorithm):
    """Given an input directory, detect sources from the science image at the lowest frequency
     and write 3 files.\n
    1) link.json: file used to link statistics files for further visualizations\n
    2) flux_freq.csv: source and file wise flux measurements for detected sources\n
    3) sources.csv: Contains source position, flux and spectral index measurements  """

    science_files = glob.glob(input_dir + "/*.pbcor.tt0.subim.fits")

    if len(science_files) == 0:
        raise click.BadParameter('No science images found in directory')

    # get the lowest frequency science image
    low_sci_name = cu.get_image_with_least_freq(science_files)
    # get corresponding rms image
    rms_img = cu.sci_to_rms(low_sci_name)
    # load science image
    low_sci_img = cu.load_fits(low_sci_name)
    

    if algorithm == "aperture":
        logging.info("Initiating aperture DAO algorithm")
        source_finder = ApertureDAO(science_files)
    #

    # Get source positions
    sources = source_finder.get_sources(low_sci_img, rms_img)

    # Flux values accross files and sources
    fluxs = source_finder.get_fluxs(sources)

    # Positions, flux value at lowest image and spectral index.
    summary = source_finder.get_summary(fluxs)

    
    results_index = {
        "science_file": low_sci_name,
        "flux_freq_file": path.join(output_dir, "flux_freq.csv"),
        "summary_file": path.join(output_dir, output_file_name)
    }
    

    with open(path.join(output_dir, "link.json"), "w") as json_file:
        json.dump(results_index, json_file)
        
        
    try:
        fluxs.to_csv(results_index["flux_freq_file"], index=False)
        summary.to_csv(results_index["summary_file"], index=False)
    except Exception as e:
        logging.exception("Error writing files to disk")
        
    
    

    logging.info(
        f"Source detection algorithm: {algorithm} successful, refer to link.json for save details")


if __name__ == "__main__":
    client = Client()
    fitsviz()
    client = client.close()
