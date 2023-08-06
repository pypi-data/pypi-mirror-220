import numpy as np
from bokeh.plotting import figure, show
from bokeh.models import LinearColorMapper, HoverTool, ColumnDataSource
from bokeh.palettes import Viridis256
from photutils.aperture import CircularAperture
from fitsviz.utils import cutils as cu
from fitsviz.detection import ap_photometry


def visualize_bokeh(sci_img):
    """_summary_

    Args:
        sci_img (_type_): _description_
    """
    # open science and rms image
    sci_data = cu.load_fits(sci_img)
    rms_data = cu.load_fits(cu.sci_to_rms(sci_img))

    # get the list of sources and the mean
    sources, mean = ap_photometry.get_sources(sci_data, rms_data)

    # list of positions to visualize
    positions = np.transpose((sources['xcentroid'], sources['ycentroid']))
    # point circles at them
    apertures = CircularAperture(positions, r=100.0)

    p = figure(
        title="Lowest frequency image: {sci_img} with sources", x_axis_label="x", y_axis_label="y")

    image_range = (np.min(sci_data - mean), np.max(sci_data - mean))
    color_mapper = LinearColorMapper(
        palette=Viridis256, low=image_range[0], high=image_range[1])
    p.image(image=[sci_data - mean], x=0, y=0, dw=sci_data.shape[1], dh=sci_data.shape[0],
            color_mapper=color_mapper)

    # Create a ColumnDataSource for the sources inside the circles
    circle_sources = ColumnDataSource(data=dict(x=[], y=[], flux=[], peak=[]))
    circle_glyph = p.circle(x='x', y='y', radius=100, line_color='black', line_width=1.5, line_alpha=1.0,
                            fill_color='rgba(0, 0, 255, 0)', source=circle_sources)

    # Set up hover tool with columns of sources
    hover = HoverTool(renderers=[circle_glyph], tooltips=[('X Centroid', '@x'),
                                                          ('Y Centroid', '@y'),
                                                          ('Flux', '@flux'),
                                                          ('Peak', '@peak')],
                      mode='mouse', point_policy='snap_to_data')

    # Add hover tool to the plot
    p.add_tools(hover)

    # Update the ColumnDataSource with sources inside the circles
    circle_sources.data = dict(x=sources['xcentroid'], y=sources['ycentroid'],
                               flux=sources['flux'], peak=sources['peak'])

    show(p)
