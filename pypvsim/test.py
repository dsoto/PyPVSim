import pypvsim
import numpy as np
import scipy as sp
from numpy.testing import assert_almost_equal

def test_dummy():
    assert 1==1

def test_solar_dummy():
    solar = pypvsim.Solar()
    date = np.datetime64('2013-01-01T12:00Z')
    dbr = solar.direct_beam_radiation(date.astype(object))
    assert dbr>0.0


def test_solar_declination():
    '''
    declination should be 23.45 degrees on summer solstice
    '''
    solar = pypvsim.Solar()
    date = np.datetime64('2013-06-21T12:00Z')
    declination = solar.declination(date.astype(object))
    assert_almost_equal(declination, sp.radians(23.45), 5)

def test_solar_declination():
    '''
    sun should be directly overhead on the equator at noon on the
    equinox
    TODO: why is the agreement so low?
    '''
    solar = pypvsim.Solar(lat=0)
    date = np.datetime64('2013-03-20T12:00Z')
    assert_almost_equal(solar.elevation(date.astype(object)),
                        sp.radians(90), 2)
    date = np.datetime64('2013-09-22T12:00Z')
    assert_almost_equal(solar.elevation(date.astype(object)),
                        sp.radians(90), 2)

