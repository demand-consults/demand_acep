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
    """
        This function reads and extracts the NetCDF format data of the given meter channel using a package called xarray.

        Parameters
        ----------
        dirpath :
            `dirpath` is the directory path location of the NetCDF file to be read
        filename :
            `filename` is the NetCDF format meter channel file to be read.

        Returns
        -------
        Dataframe
            Sample-time indexed pandas dataframe containing measurement values from the given file.
        """
    # Extracts NetCDF files using xarray module
    netcdf_data = xr.open_dataset(os.path.join(dirpath, filename))
    netcdf_df = netcdf_data.to_dataframe()
    # Converts the time index to datetime format
    netcdf_df.set_index(pd.to_datetime(netcdf_df.index.values), inplace=True)

    return netcdf_df


def extract_ppty(filename, meter_name):
    """
        This function parses out the given filename as a string to determine the meter name and the measurement
        channel/type contained in the file

        Parameters
        ----------
        filename :
            `filename` is the NetCDF format meter channel file whose name contains information such as location, date,
            meter type, measurement channel/type and sampling frequency. An example filename is:
            'PokerFlatResearchRange-PokerFlat-PkFltM1AntEaDel@2018-07-02T081007Z@PT23H@PT146F.nc'
        meter_name :
            `meter_name` is a list containing the names of each of the meters at pokerflats

        Returns
        -------
        meter : string
            `meter` is the meter name of the NetCDF format file given.
        channel : string
            `channel` is the measurement type contained in the NetCDF format file given
        """
    # Example filename - 'PokerFlatResearchRange-PokerFlat-PkFltM1AntEaDel@2018-07-02T081007Z@PT23H@PT146F.nc'
    filename_split_1 = filename.split('@')
    filename_split_2 = filename_split_1[0].split('-')
    meter_channel = filename_split_2[-1]
    for name in meter_name:
        if meter_channel.startswith(name):
            n_name = len(name)
            # Example meter from example filename above - PkFltM1Ant
            meter = meter_channel[:n_name]
            # Example channel from example filename above - EaDel (Energy delivered to Phase A)
            channel = meter_channel[n_name:]

    return meter, channel


def data_resample(df, sample_time='1T'):
    """
        This function downsamples a sample-time indexed pandas dataframe containing measurement channel values based
        on the sample time supplied. It uses the mean of the values within the resolution interval. It uses the pandas
        dataframe module `df.resample`

        Parameters
        ----------
        df :
            `df` is a sample-time indexed pandas dataframe containing measurement values from the different channels of
            each meter.
        sample_time :
            `sample_time` determines the desired resolution of the downsampled data. For 1 minute - 1T, 1 hour - 1H,
            1 month - 1M, 1 Day - 1D etc. The default chosen here is 1 minute.

        Returns
        -------
        Dataframe
            Resampled-time indexed pandas dataframe containing downsampled measurement values from the given dataframe.
        """
    # Data is downsampled using the mean of the values within the interval of the sample time provided.
    # The mean is used because it provided the average/expected value of the measurement within that time range.
    df_resampled = df.resample(sample_time, closed="left", label="right").mean()

    return df_resampled


def data_impute(impute_df, interp_method, interp_order):
    """
        This function imputes missing measurement data in the positions with NaN using the supplied interpolation method
        and order. It uses the pandas module `df.interpolate`

        Parameters
        ----------
        impute_df :
            `impute_df` can either be a dataframe of a dictionary of dataframes containing missing measurements values.
        interp_method :
            `interp_method` determines the interpolation method to be used. It can be linear, cubic, spline, etc.
        interp_order :
            `interp_order` determines the order/degree of the interpolation method chosen.

        Returns
        -------
        Dataframe
            Filled pandas dataframe with no missing values.
        """
    if isinstance(impute_df, dict):
        for meter in impute_df:
            if impute_df[meter].isnull().values.any():
                impute_df[meter] = impute_df[meter].interpolate(method=interp_method, order=interp_order)
    else:
        if impute_df.isnull().values.any():
            impute_df = impute_df.interpolate(method=interp_method, order=interp_order)

    return impute_df

