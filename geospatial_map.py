#!/usr/bin/env python3
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.animation import FuncAnimation, FFMpegWriter

def geospatial_map():

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
    relcsv = '/states_no_wa.csv'
    relshape = '/us_states/cb_2018_us_state_500k.shp'
    csvfile = cwd + relcsv 
    shapefile = cwd + relshape 

    df = pd.read_csv(csvfile, dtype=our_cols, usecols=clist)

    pd.set_option('display.max_rows', 200)
    pd.options.display.float_format='{:,.2f}'.format

    df.rename(columns=to_rename, inplace=True)
    df['State'] = df['State'].fillna('Washington').astype('category')
    df['Year'] = df['Year'].fillna(0).astype(int)
    df['Money'] = df['Money'].fillna(0).astype(float)

    """ pivoting table aggregates values by year """
    dfp = df.pivot_table(index='State', columns='Year', values='Money', observed=False, aggfunc='sum')
    dfp = dfp.fillna(value=0).astype(float)

    first_yr = dfp.columns[0]            #    2016
    last_yr = dfp.columns[-1]            #    2023
    total_mean = dfp.mean().mean()       # 391,133
    total_median = dfp.median().median() # 141,594

    """ aggregates all annual figures into total aggregate column """
    dfp['8 year total'] = dfp[2016].astype(float)
    for year in range(first_yr, (last_yr + 1), 1):
        dfp['8 year total'] += dfp[year]

    years = dfp.columns

    """ loads the shape file and merges it with the dataset """
    shape = gpd.read_file(shapefile)
    shape = pd.merge(
        left=shape,
        right=dfp,
        left_on='NAME',
        right_on='State',
        how='right'
    )

    fig, ax = plt.subplots(figsize=(12, 8))

    xlim = (shape.total_bounds[0], shape.total_bounds[2])
    ylim = (shape.total_bounds[1], shape.total_bounds[3])
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    boundary = shape.boundary.plot(ax=ax, edgecolor='black', linewidth=0.3)

    all_cols_min = dfp.iloc[:, 0:8].min().min()
    all_cols_max = dfp.iloc[:, 0:8].max().max()  # ~6M, no movement
    upper_bounds = (total_median * 2)  

    norm = plt.Normalize(vmin=all_cols_min, vmax=upper_bounds)
    comma_fmt = FuncFormatter(lambda x, _: f'${round(x, -3):,.0f}')

    sm = plt.cm.ScalarMappable(cmap='RdBu_r', norm=norm)
    sm.set_array([])  # Only needed for adding the colorbar
    colorbar = fig.colorbar(sm, ax=ax, orientation='horizontal', shrink=0.7, format=comma_fmt)

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

    years = dfp.columns[1:]  # Skip the 'State' column, [1:-1] to omit 8-yr total
    animation = FuncAnimation(fig, animate, frames=years, repeat=True, interval=1000)

    ffmpeg = FFMpegWriter(fps=1)
    with ffmpeg.saving(fig, 'recordings/out_of_state_lobby_money_geospatial_map.mp4', dpi=600):
        for year in years :
            animate(year)
            ffmpeg.grab_frame()

    with ffmpeg.saving(fig, 'recordings/out_of_state_lobby_money_geospatial_map.gif', dpi=300):
        for year in years :
            animate(year)
            ffmpeg.grab_frame() 
            print(f'recording year {year}')
        print(f'recording {os.path.basename(__file__)} complete')    

    plt.show()

if __name__ == '__main__':
    geospatial_map()