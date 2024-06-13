#!/usr/bin/env python3
import os
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

def geospatial_map():
    print('uncomment docstring at bottom if you want to create a recording')
    our_cols = {
        'State': 'category',
        'Year': 'int',
        'Money': 'float',
    }

    to_rename = {
        'Unnamed: 0':'position',
    }

    clist = []
    for col in our_cols:
        clist.append(col)

    cwd = os.getcwd()
    relativecsv = '/states_no_wa.csv'
    relativeshape = '/us_states/cb_2018_us_state_500k.shp'
    csvfile = cwd + relativecsv 
    shapefile = cwd + relativeshape 

    df = pd.read_csv(csvfile, dtype=our_cols, usecols=clist)

    pd.set_option('display.max_rows', 200)
    pd.options.display.float_format='{:,.2f}'.format

    df.rename(columns=to_rename, inplace=True)
    df['State'] = df['State'].fillna('Washington').astype('category')
    df['Year'] = df['Year'].fillna(0).astype(int)
    df['Money'] = df['Money'].fillna(0).astype(float)

    dfp = df.pivot_table(index='State', columns='Year', values='Money', observed=False)
    dfp = dfp.fillna(value=0).astype(float)

    dfp['8 year total'] = dfp[2016].astype(float)
    for year in range(2017, 2023, 1):
        dfp['8 year total'] += dfp[year]

    years = dfp.columns
    shape = gpd.read_file(shapefile)
    shape = pd.merge(
        left=shape,
        right=dfp,
        left_on='NAME',
        right_on='State',
        how='right'
    )

    fig, ax = plt.subplots(figsize=(15, 8))

    xlim = (shape.total_bounds[0], shape.total_bounds[2])
    ylim = (shape.total_bounds[1], shape.total_bounds[3])
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    boundary = shape.boundary.plot(ax=ax, edgecolor='black', linewidth=0.3)
    norm = plt.Normalize(vmin=dfp.iloc[:, 1:7].min().min(), vmax=dfp.iloc[:, 1:7].max().max())

    sm = plt.cm.ScalarMappable(cmap='RdBu_r', norm=norm)
    sm.set_array([])  # Only needed for adding the colorbar
    colorbar = fig.colorbar(sm, ax=ax, orientation='horizontal', shrink=0.5, format='%.0f')

    def animate(year):
        ax.clear()

        ax.set_title(
            f'Money from other states used to lobby Washington ({year})', 
            size=18, weight='bold'
        )

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        for surface in ['top', 'right', 'bottom', 'left']:
            ax.spines[surface].set_visible(False)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        boundary = shape.boundary.plot(ax=ax, edgecolor='black', linewidth=0.3)
        
        shape.plot(
            ax=ax, column=year, legend=False, cmap='RdBu_r', norm=norm
        )

    years = dfp.columns[1:]  # Skip the 'State' column
    animation = FuncAnimation(fig, animate, frames=years, repeat=True, interval=1000)

    """ Save the animation as a GIF 
    writer = PillowWriter(fps=1)
    animation.save('../recordings/wa_out_of_state_lobbying_geospatial_anim.gif', writer=writer)
    or can use ffmpeg - slightly different process
    note: ffmpeg is is extension-aware (mp4, gif, avi, mkv, etc.)
    ffmpeg = FFMpegWriter(fps=1)
    with ffmpeg.saving(fig, '../recordings/horizontal_bar_chart_animation.mp4', dpi=600):
        for year in years :
            animate(year)
            ffmpeg.grab_frame()
    plt.close()  # if you only want to save the animation - comment out plt.show()
    """
    plt.show()

if __name__ == '__main__':
    geospatial_map()