"""
File containing bokeh backend plots
"""
import numpy as np
from bokeh.plotting import figure, show
from bokeh.models import LinearColorMapper, HoverTool, ColumnDataSource
from bokeh.palettes import Viridis256
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot
from bokeh.models import HoverTool
from photutils.aperture import CircularAperture
from fitsviz.utils import cutils as cu
from fitsviz.detection import ap_photometry


def visualize_source(sci_file, sources):
    """Visualize lowest frequency science FITS file interactively in Bokeh.
    FITS file is plotted with circles indicating sources, which can be zoomed in the html file.

    Args:
        sci_file (str): file name of science FITS file
        sources (pd.DataFrame): DataFrame with xcentroid,ycentroid,flux,spectral_index

    Returns:
        bokeh.plotting.figure: Bokeh object containig plotted file
    """
    # open science and rms image
    sci_data = cu.load_fits(sci_file)
    rms_data = cu.sci_to_rms(sci_file)

    # get the list of sources and the mean
    mean = np.nanmean(rms_data)
    fig = figure(
        title=f"Lowest frequency image: {sci_file} with sources", x_axis_label="x", y_axis_label="y")
    # set color ranges
    image_range = (np.min(sci_data - mean), np.max(sci_data - mean))
    color_mapper = LinearColorMapper(
        palette=Viridis256, low=image_range[0], high=image_range[1])

    # plot mean subtracted image
    fig.image(image=[sci_data - mean], x=0, y=0, dw=sci_data.shape[1], dh=sci_data.shape[0],
              color_mapper=color_mapper)

    # Create a ColumnDataSource for the sources inside the circles
    circle_sources = ColumnDataSource(data=dict(x=[], y=[], flux=[], peak=[]))
    circle_glyph = fig.circle(x='x', y='y', radius=100, line_color='black', line_width=1.5, line_alpha=1.0,
                              fill_color='rgba(0, 0, 255, 0)', source=circle_sources)

    # Set up hover tool with columns of sources
    hover = HoverTool(renderers=[circle_glyph], tooltips=[('X Centroid', '@x'),
                                                          ('Y Centroid', '@y'),
                                                          ('Flux', '@flux'),
                                                          ('spectral index', '@spectral_index')],
                      mode='mouse', point_policy='snap_to_data')

    # Add hover tool to the plot
    fig.add_tools(hover)

    # Update the ColumnDataSource with sources inside the circles
    circle_sources.data = dict(x=sources['xcentroid'], y=sources['ycentroid'],
                               flux=sources['flux'], peak=sources['spectral_index'])

    show(fig)
    return fig


def grid_view(sci_file, sources):
    """
    Grid view of all sources in lowest frequency science FITS file

    Args:
        sci_file (str): file name of science FITS file
        sources (pd.DataFrame): DataFrame with xcentroid,ycentroid,flux,spectral_index

    Returns:
        bokeh.models.plots.GridPlot: Bokeh plot containing all sources
    """

    # Load science and rms files
    sci_data = cu.load_fits(sci_file)
    rms_data = cu.sci_to_rms(sci_file)

    # get mean and positions
    mean = np.nanmean(rms_data)
    positions = np.transpose((sources['xcentroid'], sources['ycentroid']))

    plots = []

    for i in range(len(positions)):
        x = int(positions[i][0])
        y = int(positions[i][1])

        # Extract a 300x300 region centered at the circle
        region = sci_data[y-150:y+150, x-150:x+150]

        # Calculate statistics for the circle
        flux = sources['flux'][i]
        spectral_index = sources['spectral_index'][i]
        xcentroid = sources['xcentroid'][i]
        ycentroid = sources['ycentroid'][i]

        # Create a new plot for each circle
        fig = figure(title=f"Plot {i+1}\n x:{xcentroid}, y:{ycentroid}",
                     x_axis_label="x", y_axis_label="y", width=300, height=300)

        # Set up hover tool with columns of sources at the center
        hover = HoverTool(tooltips=[('X Centroid', str(xcentroid)),
                                    ('Y Centroid', str(ycentroid)),
                                    ('Flux (Jy)', str(flux))])

        # Plot the extracted region
        fig.image(image=[region - mean], x=0, y=0,
                  dw=region.shape[1], dh=region.shape[0])

        # Add hover tool to the plot
        fig.add_tools(hover)

        plots.append(fig)

    grid = gridplot(plots, ncols=3)

    show(grid)
    return grid


def plot_flux_freq(flux_df, sources):
    """
        Flux vs frequency plot of detected astronomical sources.

    Returns:
        bokeh.models.plots.GridPlot: Bokeh plot containing all sources
    Args:
        flux_df (np.ndarray): pandas DataFrame containing frequencies of the detected objects as columns
        and rows indicating flux of each source.

        sources (pd.DataFrame): DataFrame with xcentroid,ycentroid,flux,spectral_index

    Returns:
        Bokeh object containig plotted files
    """

    freqs = list(flux_df.columns)

    plots = []
    for idx, row in flux_df.iterrows():
        # Create a new figure for each row
        image_title = f"Source: {sources.xcentroid[idx],sources.xcentroid[idx]}, Spectral index = {sources.spectral_index[idx]}"
        p = figure(title=image_title, x_axis_label="Frequency (GHz)",
                   y_axis_label="Flux (Jy)", width=500, height=500)

        # Plot frequency  vs flux
        p.scatter(freqs, row.values)

        # Add the hover tool with x and y information
        hover = HoverTool(
            tooltips=[("Frequency (GHz)", "@x"), ("Flux (Jy)", "@y")], mode="vline")
        p.add_tools(hover)

        # Add the plot to the ist
        plots.append(p)

        # Create a grid of plots with 2 columns
    grid = gridplot(plots, ncols=3)
    show(grid)

    # Show the grid of plots
    return grid
