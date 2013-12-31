from . import pvsim
import numpy as np
import matplotlib.pyplot as plt

def pin_path():
    print('pin path')
    return 0

def plot_sun_path(lat=30, ax=None):
    if ax==None:
        fig, ax = plt.subplots()
        return_ax = False
    else:
        return_ax = True

    solar = pvsim.Solar(lat=lat)
    # create a range of months and create a timestamps throughout the day on the 21st
    # to coincide with solstice
    months = range(6, 13)
    datesdict = {'{0:0>2}-21'.format(m):
                np.arange('2013-{0:0>2}-21T00:00:00Z'.format(m),
                          '2013-{0:0>2}-22T00:00:00Z'.format(m),
                          np.timedelta64(10,'m'),
                          dtype='datetime64') for m in months}
    # plot each array using the key as a label
    for k,v in datesdict.items():
        azimuth = np.degrees([solar.azimuth(d.astype(object)) for d in v])
        elevation = np.degrees([solar.elevation(d.astype(object)) for d in v])
        ax.plot(azimuth, elevation, label=k, color='k')
        # TODO: this text placement is crazy fragile and ugly.  improve.
        ax.text(azimuth[72], elevation[72], k)

    # create time ranges using a dictionary comprehesnsion
    times = range(6,19)
    timedict={t:np.arange('2013-06-21T{0:0>2}:00:00Z'.format(t),
                          '2013-12-21T{0:0>2}:00:00Z'.format(t),
                          np.timedelta64(10,'D'),
                          dtype='datetime64') for t in times}
    for k,v in timedict.items():

        azimuth = np.degrees([solar.azimuth(d.astype(object)) for d in v])
        elevation = np.degrees([solar.elevation(d.astype(object)) for d in v])
        ax.plot(azimuth, elevation, label=k, color='k')
        # tweak hour labels
        if azimuth[0] > 0:
            azloc = azimuth[0] + 3
        else:
            azloc = azimuth[0] - 10
        ax.text(azloc, elevation[0], k)
    ax.set_ylim((0, 95))
    ax.set_yticks(np.linspace(0, 90, 10))
    ax.set_xlabel('Solar Azimuth (deg)')
    ax.set_ylabel('Solar Altitude (deg)')
    ax.grid()
    if return_ax:
        return ax
    else:
        plt.show()
