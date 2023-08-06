# pylint: disable=invalid-syntax
# use logging to print messages to the console
import dask
from fitsviz.utils import cutils as cu
from fitsviz.detection.ap_photometry import ApertureDAO
from fitsviz.viz import plot_bokeh, plot_matplotlib
import click
import glob
from os import path
import numpy as np
import logging
from astropy.io import fits

logging.basicConfig(level=logging.INFO)


@click.group()
def fitsviz():
    """fitsviz: Autodetection of sources and visualization of FITS files"""


@fitsviz.command()
@click.option('input_dir', '-i', type=click.Path(exists=True), nargs=1)
@click.option('backend', '-b', '--backend', default='matplotlib',
              type=click.Choice(['matplotlib', 'bokeh']), help='Visualization backend')
def mkviz(input_dir, backend):
    """visualize the lowest frequency science image in a directory"""

    science_files = glob.glob(input_dir + "/*.pbcor.tt0.subim.fits")
    if len(science_files) == 0:
        raise click.BadParameter('No science images found in directory')
    low_sci = cu.get_image_with_least_freq(science_files)

    if backend == 'bokeh':
        plot_bokeh()
    else:
        plot_matplotlib.da_visualize(low_sci, cu.sci_to_rms(low_sci))


@fitsviz.command()
@click.option('input_dir',
               '-i',
                 type=click.Path(exists=True))
@click.option('output_dir',
              '-od',
              type=click.Path(exists=True),
              default='data')
@click.option('output_file_name', '-o', '--output_file_name',
              default='sources.csv', help='detected CSV file name')
@click.option("algorithm",
              "-a",
              "--algorithm",
              default="aperture",
              type=click.Choice(["aperture","custom"]),
              help="source detection algorithm")

def mkstat(input_dir, output_dir, output_file_name, algorithm):
    """identify objects from the science image at the lowest frequency"""
    science_files = glob.glob(input_dir + "/*.pbcor.tt0.subim.fits")

    if len(science_files) == 0:
        raise click.BadParameter('No science images found in directory')
    # get the lowest frequency science image
    low_sci_name = cu.get_image_with_least_freq(science_files)

    rms_img = cu.sci_to_rms(low_sci_name)

    low_sci_img = cu.load_fits(low_sci_name)
    if algorithm == "aperture":

        source_finder = ApertureDAO()
        sources = source_finder.get_sources(low_sci_img, rms_img)
        # Compute dask graph
        summary = source_finder.process_sources(sources, science_files)
        # Write sources file to csv
        
        out_path = path.join(output_dir, output_file_name)
        summary.to_csv(out_path, index=False)

        logging.info(f"Source detection algorithm: {algorithm} successful, saved to {out_path}")


if __name__ == "__main__":
    fitsviz()
