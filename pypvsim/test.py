import pypvsim
import numpy as np
import scipy as sp
from numpy.testing import assert_almost_equal

def test_solar_declination():
    '''
    declination should be 23.45 degrees on summer solstice
    '''
    solar = pypvsim.Solar()
    date = np.datetime64('2013-06-21T12:00Z')
    declination = solar.declination(date.astype(object))
    assert_almost_equal(declination, sp.radians(23.45), 5)

def test_solar_elevation():
    '''
    sun should be directly overhead on the equator at noon on the
    equinox
    '''
    # TODO: why is the decimal agreement so low?
    solar = pypvsim.Solar(lat=0)
    date = np.datetime64('2013-03-20T12:00Z')
    assert_almost_equal(solar.elevation(date.astype(object)),
                        sp.radians(90), 1)
    date = np.datetime64('2013-09-22T12:00Z')
    assert_almost_equal(solar.elevation(date.astype(object)),
                        sp.radians(90), 1)

def test_panel_incidence_angle():
    '''
    angle of zero for normal elevation panel on the equator with sun
    directly overhead
    '''
    solar = pypvsim.Solar(lat=0)
    panel = pypvsim.Panel(solar, el_tilt=0)
    date = np.datetime64('2013-03-20T12:00Z')
    assert_almost_equal(panel.incidence_angle(date.astype(object)),
                        0, 1)

    # TODO: what should incidence angle be here?
    solar = pypvsim.Solar(lat=45)
    panel = pypvsim.Panel(solar, el_tilt=45, az_tilt=45)
    date = np.datetime64('2013-03-20T12:00Z')
    #assert_almost_equal(panel.incidence_angle(date.astype(object)),
    #                    sp.radians(45), 1)

def test_panel_radiation():
    '''
    angle of zero for normal elevation panel on the equator with sun
    directly overhead
    '''
    solar = pypvsim.Solar(lat=0)
    panel = pypvsim.Panel(solar, el_tilt=0)
    date = np.datetime64('2013-03-20T12:00Z')
    assert_almost_equal(panel.incidence_angle(date.astype(object)),
                        0, 1)

def test_azimuth():
    solar = pypvsim.Solar(lat=40)
    # zero at noon
    assert_almost_equal(solar.azimuth(np.datetime64('2013-01-01T12:00Z').astype(object)),
                        0.0)
    assert_almost_equal(solar.azimuth(np.datetime64('2013-06-21T12:00Z').astype(object)),
                        0.0)

    # due west at 6pm on the equinox
    assert_almost_equal(solar.azimuth(np.datetime64('2013-03-21T18:00Z').astype(object)),
                        np.radians(90), 1)
    # test southern hemisphere
    solar = pypvsim.Solar(lat=-40)
    assert_almost_equal(solar.azimuth(np.datetime64('2013-03-21T18:00Z').astype(object)),
                        np.radians(90), 1)


def test_elevation():
    solar = pypvsim.Solar(lat=40)

# TODO: check angles in general
def test_load_supply():
    load   = np.array([0, 0, 0, 0, 1, 2, 2, 1, 0, 0])
    supply = np.array([0, 0, 1, 1, 2, 2, 0, 0, 0, 0])
    dt = 1

    assert pypvsim.excess_demand(load, supply, 1) == 3
    assert pypvsim.excess_supply(load, supply, 1) == 3
    assert pypvsim.fraction_excess_supply(load, supply, dt) == 0.5
    assert pypvsim.fraction_excess_demand(load, supply, dt) == 0.5

def test_run_simulation():
    lead_dict = {'type' : 'lead acid',
             'cost' : 0.14,
             'battery_efficiency_curve' : {'output_power':[0, 1000],
                                           'efficiency':[0.75,   0.75]},
             'DOD' : 0.5,
             'life' : 2
             }
    result = pypvsim.run_simulation(lead_dict,
                           inverter_type='typical',
                           load_type='day',
                           plot=False, verbose=False)
    assert_almost_equal(result['battery_cost'],
                        213.46715017)
    assert_almost_equal(result['battery_size_kWh'],
                        0.76238267918374858)
    result = pypvsim.run_simulation(lead_dict,
                                    inverter_type='typical',
                                    load_type='night',
                                    plot=False, verbose=False)
    assert_almost_equal(result['battery_cost'],
                        1376.3846808510641)
    assert_almost_equal(result['battery_size_kWh'],
                        4.9156595744680853)

