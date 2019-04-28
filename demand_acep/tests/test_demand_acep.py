"""
This is the place for all the unit tests for the package demand_acep.
We can refactor this if this becomes too large.

"""

import pandas as pd
import numpy as np
import os
import sys
import re
from os import listdir
from os.path import isfile, join
import pytest # automatic test finder and test runner


# To import files from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from demand_acep import hello_world
from read_NetCDF import extract_data
from read_NetCDF import extract_ppty

def test_hello_world():
    """
    This function test the function hello_world()
    """
    print('Hello World yass!')
    result = hello_world()

    assert result == "Hello world!", "The function does not return the string 'Hello world!'"

    return


def test_extract_data():
    dirpath = '/Volumes/GoogleDrive/My Drive/ACEP/Data/2018/07/01'
    filename = 'PokerFlatResearchRange-PokerFlat-PkFltM1AntEaDel@2018-07-01T081005Z@P1D@PT151F.nc'
    [test_time, test_values] = extract_data(dirpath, filename)

    assert (test_time.dtype == 'timedelta64[ns]'), "The first output from this function should be a timedelta object"

    assert isinstance(test_values, np.ndarray), "The second output from this function should be a numpy array"

    return


def test_extract_ppty():
    meter_name = ['PkFltM1Ant', 'PkFltM2Tel', 'PkFltM3Sci', 'PQube3']
    filename = 'PokerFlatResearchRange-PokerFlat-PkFltM1AntEaDel@2018-07-01T081005Z@P1D@PT151F.nc'
    [test_meter, test_channel] = extract_ppty(filename, meter_name)

    assert (any(val == test_meter for val in meter_name)), "Returned meter name does not exist"

    assert (test_channel in filename), "Returned measurement channel does not exist"

    return
