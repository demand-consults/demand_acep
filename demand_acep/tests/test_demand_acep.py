"""
This is the place for all the unit tests for the package demand_acep.
We can refactor this if this becomes too large.

"""
# %% Imports

import os
import sys
import numpy as np
import pdb

# To import files from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from demand_acep import extract_data
from demand_acep import extract_ppty
from demand_acep import data_resample
# %% Paths


def test_extract_data():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    dirpath = os.path.join(path, 'data/measurements/2018/07/01')
    filename = 'PokerFlatResearchRange-PokerFlat-PkFltM1AntEaDel@2018-07-02T081007Z@PT23H@PT146F.nc'
    test_df = extract_data(dirpath, filename)
    column_name = test_df.columns.tolist()[0]

    assert (test_df.index.dtype == 'datetime64[ns]'), "The first output from this function should be a timedelta object"

    assert (test_df[column_name].dtype == 'float64'), "The second output from this function should be a numpy array"

    return


def test_extract_ppty():
    meter_name = ['PkFltM1Ant', 'PkFltM2Tel', 'PkFltM3Sci', 'PQube3']
    filename = 'PokerFlatResearchRange-PokerFlat-PkFltM1AntEaDel@2018-07-02T081007Z@PT23H@PT146F.nc'
    [test_meter, test_channel] = extract_ppty(filename, meter_name)

    assert (any(val == test_meter for val in meter_name)), "Returned meter name does not exist"

    assert (test_channel in filename), "Returned measurement channel does not exist"

    return


def test_data_resample():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    dirpath = os.path.join(path, 'data/measurements/2018/07/01')
    filename = 'PokerFlatResearchRange-PokerFlat-PkFltM1AntEaDel@2018-07-02T081007Z@PT23H@PT146F.nc'
    test_df = extract_data(dirpath, filename)
    test_resampled = data_resample(test_df, sample_time='1T')
    diff_test = np.diff(test_resampled.index)
    time_1T_ns = np.timedelta64(60000000000,'ns') # sample_time 1T in nanoseconds
    assert (np.all(np.equal(diff_test, time_1T_ns))), "Data not properly resampled"

    return
