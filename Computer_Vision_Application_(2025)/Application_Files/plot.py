# plot.py
# Created by Ariana Beeby, Max Figura, and Jason Jopp for CSC443
# Creates visualizations for data found in the program

import numpy as np
import os
import pandas as pd
import plotly.express as px
import colorsys


def hsv_color_range(lower, upper):
    """
    Given an upper and lower HSV color value, creates a 3d plot displaying the
    selected color space contained within those two values, writes to .cache dir

    Parameters
    ----------
    lower : tuple
        The lower HSV color code: (<hue:int>, <sat:int>, <val:int>)
    upper : tuple
        The upper HSV color code: (<hue:int>, <sat:int>, <val:int>)
    
    Returns
    ----------
    Write: .cache/color_space.png
        Writes a png of the color space to the .cache folder
    """

    # Samples across HSV color space, finds interior values of color space
    hue_sample = np.linspace(lower[0], upper[0], 3)
    sat_sample = np.linspace(lower[1], upper[1], 3)
    val_sample = np.linspace(lower[2], upper[2], 3)

    # Creates a grid object holding the sampled values
    grid = np.meshgrid(hue_sample, sat_sample, val_sample)

    # These variables hold data that will be used to construct a dataframe  
    h = []
    s = []
    v = []
    id = []
    color_codes = []
    i = 0

    # Fills arrays with data require to create dataframe
    for val in np.nditer(grid):
        h.append(val[0])
        s.append(val[1])
        v.append(val[2])

        # Converts HSV values into RGB for plotting        
        r, g, b = colorsys.hsv_to_rgb(val[0] / 360, val[1] / 255, val[2] / 255)
        color_codes.append(f"rgb({round(r*255)},{round(g*255)},{round(b*255)})")

        # id keeps track of which glyph will be what color
        id.append(str(i))
        i += 1

    # Creates the dataframe using the data
    df = pd.DataFrame({'hue': h, 
                       'val': s, 
                       'sat': v,
                       'id': id,
                       'color_code': color_codes})

    # Generates a 3d plot using the dataframe
    fig = px.scatter_3d(df, x="hue", y="val", z="sat",
                        color = color_codes,
                        color_discrete_map = "identity")
    
    fig.update_traces(marker = dict(size = 13,
                                    line = dict(width = 2, color = "black")))
    
    # Change the background color to light grey, so it's not blue
    # Changes the margins of the background grids to not overlap with points.
    fig.update_layout(
        scene=dict(
            xaxis=dict(backgroundcolor="lightgrey",
                       range = [lower[0]-10, upper[0]+10]),
            yaxis=dict(backgroundcolor="lightgrey",
                       range = [lower[1]-10, upper[1]+10]),
            zaxis=dict(backgroundcolor="lightgrey",
                       range = [lower[2]-25, upper[2]+19]),
        )
    )
    
    # Modifies starting camera position, axis labels in plot, margins of image
    fig.update_layout(
        scene_camera = dict(
            eye = dict(x = 1.5, y = 1.9, z = 0.8)
        ),
        width=500, 
        height=500,
        scene = dict(
                      xaxis=dict(
                          title=dict(
                              text='Hue'
                          ),
                          title_font=dict(size=20),
                          tickfont=dict(size=14)
                      ),
                      yaxis=dict(
                          title=dict(
                              text='Value'
                          ),
                          title_font=dict(size=20),
                          tickfont=dict(size=14)
                      ),
                      zaxis=dict(
                          title=dict(
                              text='Saturation'
                          ),
                          title_font=dict(size=20),
                          tickfont=dict(size=14)
                      ),
                    ),
                    margin=dict(l=25, r=25, b=25, t=0)
    )

    # Writes the image to the .cache directory
    if os.path.isdir(".cache"):
        fig.write_image(".cache/color_space.png")
    else:
        os.mkdir(".cache")
        fig.write_image(".cache/color_space.png")

    return ".cache/color_space.png"
