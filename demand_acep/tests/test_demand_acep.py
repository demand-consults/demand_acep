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
from demand_acep import data_impute
# %% Paths
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dirpath = os.path.join(path, 'data/measurements/2018/07/01')
filename = 'PokerFlatResearchRange-PokerFlat-PkFltM1AntEaDel@2018-07-02T081007Z@PT23H@PT146F.nc'


def test_extract_data():
    test_df = extract_data(dirpath, filename)
    column_name = test_df.columns.tolist()[0]

    assert (test_df.index.dtype == 'datetime64[ns]'), "The first output from this function should be a timedelta object"

    assert (test_df[column_name].dtype == 'float64'), "The second output from this function should be a numpy array"

    return


def test_extract_ppty():
    meter_name = ['PkFltM1Ant', 'PkFltM2Tel', 'PkFltM3Sci', 'PQube3']
    [test_meter, test_channel] = extract_ppty(filename, meter_name)

    assert (any(val == test_meter for val in meter_name)), "Returned meter name does not exist"

    assert (test_channel in filename), "Returned measurement channel does not exist"

    return


def test_data_resample():
    test_df = extract_data(dirpath, filename)
    test_resampled = data_resample(test_df, sample_time='1T')
    diff_test = np.diff(test_resampled.index)
    time_1T_ns = np.timedelta64(60000000000,'ns') # sample_time 1T in nanoseconds
    assert (np.all(np.equal(diff_test, time_1T_ns))), "Data not properly downsamples"

    return


def test_data_impute():
    interp_method = 'spline'
    interp_order = 2
    test_df = extract_data(dirpath, filename)
    test_df = data_impute(test_df, interp_method, interp_order)
    # pdb.set_trace()
    dict_assert = []
    if isinstance(test_df, dict):
        for meter in test_df:
            dict_assert.append(test_df[meter].notnull().values.all())
        assert (all(val for val in dict_assert)), "Data imputations in dictionary not functioning properly as data " \
                                                  "still contains NaN"
    else:
        assert (test_df.notnull().values.all()), "Data imputations in Dataframes not functioning properly as data " \
                                                 "still contains NaN"

    return
