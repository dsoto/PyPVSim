# functions for loads and tariffs

import pandas as pd
import numpy as np

def constant_load(load):
    index = pd.date_range('1/1/2014', periods=8760, freq='H')
    return pd.Series(index=index, data=np.ones(8760) * load)

def evening_load(day_load, night_load, day_hours=12):
    single_day = np.hstack((np.ones(day_hours) * day_load,
                            np.ones(24 - day_hours) * night_load))
    year = np.tile(single_day, 365)
    index = pd.date_range('1/1/2014', periods=8760, freq='H')
    return pd.Series(index=index, data=year)

# create utility to read in load file

#TODO create a general load function that creates hourly loads as a list
# maybe as a list of tuples
