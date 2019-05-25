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

def hello_world():
    """
    This function returns the string Hello World.

    This is for testing the CI and other devops functionality.

    :return: A string "Hello world!"
    """

    print("Hello WOrlds")


    return "Hello world!"


def extract_data(dirpath, filename):
    """This function takes in a filename and directory path, extracts the meter channel data in that file and
    returns the time and channel values at each time"""
    netcdf_data = xr.open_dataset(os.path.join(dirpath, filename))
    netcdf_df = netcdf_data.to_dataframe()
    netcdf_df.set_index(pd.to_datetime(netcdf_df.index.values), inplace=True)
    # pdb.set_trace()
    return netcdf_df


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


def data_resample(netcdf_df, sample_time='1T'):
    """This function accepts a dataframe and downsamples it based on the sample time supplied"""
    netcdf_resampled = netcdf_df.resample(sample_time).mean()

    return netcdf_resampled


def data_impute(impute_df, interp_method, interp_order):
    """This function accepts a dataframe or a dictionary of dataframes and imputes data in the positions with NaN
    using the supplied interpolation method and order."""
    if isinstance(impute_df, dict):
        for meter in impute_df:
            if impute_df[meter].isnull().values.any():
                impute_df[meter] = impute_df[meter].interpolate(method=interp_method, order=interp_order)
    else:
        if impute_df.isnull().values.any():
            impute_df = impute_df.interpolate(method=interp_method, order=interp_order)

    return impute_df

