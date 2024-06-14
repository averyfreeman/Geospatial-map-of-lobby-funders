#!/usr/bin/env python3
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from colour import Color

def bar_chart():

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
    relativefile = '/states_no_wa.csv'
    csvfile = cwd + relativefile 

    df = pd.read_csv(csvfile, dtype=our_cols, usecols=clist)
    
    pd.set_option('display.max_rows', 200)
    pd.options.display.float_format='{:,.0f}'.format

    df.rename(columns=to_rename, inplace=True)

    df['State'] = df['State'].fillna('Washington').astype('category')
    df['Year'] = df['Year'].fillna(0).astype(int)
    df['Money'] = df['Money'].fillna(0).astype(float)

    df = df.drop(df[df['Money'] == 0].index)

    df = df.pivot_table(index='State', columns='Year', values='Money', aggfunc='sum')

    df.sort_values(axis=0, by='State', ascending=False, inplace=True)

    df = df.fillna(value=0)
    df = df.astype(float)

    first_yr = df.columns[0]
    last_yr = df.columns[-1]  

    dfp = df.copy(deep=True)

    dfp['8 year total'] = dfp[2016].round().astype(int)
    for year in range(first_yr + 1, last_yr + 1, 1):  
        dfp['8 year total'] += dfp[year]
        dfp[year] = dfp[year].round().astype(int)

    dfpr = dfp.reset_index(col_level=0, names='State')

    dfpr = dfpr.drop(dfpr[dfpr['State'] == 'Washington'].index)
    dfpr = dfpr.drop(dfpr[dfpr['State'] == 'Wyoming'].index)
    dfpr = dfpr.drop(dfpr[dfpr['State'] == 'West Virginia'].index)
    dfpr = dfpr.drop(dfpr[dfpr['State'] == 'North Dakota'].index)

    fig, ax = plt.subplots(figsize=(14,10))

    xlim = df.max().max()
    ax.set_xlim(left=0, xmax=xlim)

    for surface in ['top', 'right', 'bottom', 'left']:
        ax.spines[surface].set_visible(False)

    ax.tick_params(left=False)
    ax.get_xaxis().set_visible(False)

    colorlist = list(Color('blue').range_to(Color('green'),21)) + list(Color('green').range_to(Color('red'),21))
    colors = []
    for color in colorlist:
        colors.append(color.hex_l)

    def animate(year):
        ax.clear()
        states = plt.barh(left=0, y=dfpr['State'], width=dfpr[year], align='center', color=colors)

        ax.bar_label(states, labels=[f'{round(value, -3):,.0f}' if value > 0 else '' for value in dfpr[year]], fmt='%.0f', color='black', alpha=0.8, padding=5, label_type='edge', font={'size': 9})

        ax.set_title(f'Money from other states used to lobby Washington {year}', size=20, weight='bold')
    
    years = dfpr.columns[1:]  # skips States column, [1:-1] omits 8-yr
    animation = FuncAnimation(fig, animate, frames=years, repeat=True, interval=1000)


    ffmpeg = FFMpegWriter(fps=1)
    with ffmpeg.saving(fig, 'recordings/out_of_state_lobby_money_bar_chart.mp4', dpi=600):
        for year in years :
            animate(year)
            ffmpeg.grab_frame()

    with ffmpeg.saving(fig, 'recordings/out_of_state_lobby_money_bar_chart.gif', dpi=300):
        for year in years :
            animate(year)
            ffmpeg.grab_frame()
            print(f'recording year {year}')
        print(f'recording {os.path.basename(__file__)} complete')    

    plt.show()
    
if __name__ == '__main__':
    bar_chart()