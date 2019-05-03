"""
This module contains code for the demand_acep. More documentation to come.

This is a test docstring for the whole module

"""

# %% Imports
import os
import pandas as pd
import pdb
import xarray as xr

# %%

def extract_data(dirpath, filename):
    """This function takes in a filename and directory path, extracts the meter channel data in that file and
    returns the time and channel values at each time"""
    netcdf_data = xr.open_dataset(os.path.join(dirpath, filename))
    netcdf_df = netcdf_data.to_dataframe()

    return netcdf_df.index, netcdf_df['value'].values


def extract_ppty(filename, meter_name):
    """This function takes in a filename and the list containing the names of each of the four meters at pokerflats;
    extracts and returns the meter name and measurement type described in the filename"""
    filename_split_1 = filename.split('@')
    filename_split_2 = filename_split_1[0].split('-')
    meter_channel = filename_split_2[-1]
    for name in meter_name:
        if meter_channel.startswith(name):
            n_name = len(name)
            meter = meter_channel[:n_name]
            channel = meter_channel[n_name:]

    return meter, channel
