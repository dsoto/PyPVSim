
# TMY3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt

'''
try:
    sr
except NameError:
    sr = pd.read_table('http://rredc.nrel.gov/solar/old_data/nsrdb/1991-2005/data/tmy3/724957TY.csv', skiprows=1, sep=',')
else:
    print('skipping download')


'''

def download_tmy_raw(USAF):
    url = 'http://rredc.nrel.gov/solar/old_data/nsrdb/1991-2005/data/tmy3/{}TY.csv'.format(USAF)
    return pd.read_table(url, skiprows=1, sep=',')

def download_tmy(USAF):
    tmydf = download_tmy_raw(USAF)
    tmydf = make_date_index(tmydf)
    return tmydf

def make_date_index(tmydf):
    # hack to get a proper datetime index
    # TODO make sure the hour handling is legit
    year = 2014
    index = []
    for d in tmydf.iterrows():
        M, D, Y = map(int, d[1]['Date (MM/DD/YYYY)'].split('/'))
        h, m = map(int, d[1]['Time (HH:MM)'].split(':'))
        index.append(dt.datetime(year, M, D, h - 1))

    tmydf.index = index
    return(tmydf)


#def heat_map(tmydf, column):
def heat_map(series):
    ''' construct heat map using numpy reshape '''
    # take column values
    #values = tmydf[column].values
    values = series.values
    # reshape
    values = values.reshape((24, 365), order='F')
    # imshow
    fig, ax = plt.subplots(1, 1)
    plot = ax.imshow(values, aspect='auto', interpolation='none')
    fig.colorbar(plot)
    #ax.set_title(column)
    plt.show()
    # labels
    # add labels and ticks for date
    # add labels and ticks for hour of day

def heat_map_groupby(tmydf, column):
    ''' construct heatmap using pandas group by '''
    values = tmydf[column].values
    sgb = values.groupby(values.index.hour)
    dfl = {}

    # this way might be expensive
    for name, group in sgb:
        dfl[name] = group.values
    mdni = pd.DataFrame(dfl).T

    # numpy reshape could be much faster, especially for interactive

    fig, ax = plt.subplots(1, 1)
    plot = ax.imshow(mdni, aspect='auto', interpolation='none')
    fig.colorbar(plot)
    plt.show()
