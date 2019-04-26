# %% Imports
import os
import re
import pandas as pd
import pdb
import netCDF4
import xarray as xr

# %% Read in files containing data type
path_struct = '/Volumes/GoogleDrive/My Drive/ACEP/UW Direct Capstone Project Files/Original Proposal Docs/Copy of Measured Channels PFRR.xlsx'
# xl_file = pd.ExcelFile(path_struct)
meter_details = pd.read_excel(path_struct)
# Extract channel names
channel_name = list(meter_details['Channels'][:48])
channel_description = list(meter_details['Desc'][:48])
channel_dict = dict(zip(channel_name, channel_description))
# Extract name of meters
meter_name = list(meter_details.columns.values)[-4:]
# %% Functions


def extract_data(dirpath, filename):
    """This function takes in a filename and directory path and extracts the required data"""
    netcdf_data = xr.open_dataset(os.path.join(path_data, filename))
    netcdf_df = netcdf_data.to_dataframe()

    return netcdf_df


def extract_ppty(filename, meter_name):
    filename_split_1 = filename.split('@')
    filename_split_2 = filename_split_1[0].split('-')
    meter_channel = filename_split_2[-1]
    for name in meter_name:
        if meter_channel.startswith(name):
            n_name = len(name)
            meter = meter_channel[:n_name]
            channel = meter_channel[n_name:]
    return meter, channel

# %% Walk through folders and read .nc files using xarray


# Create Pandas dataframe for 4 meters
# PkFltM1Ant_df = pd.DataFrame(columns=channel_name)
# PkFltM2Tel_df = pd.DataFrame(columns=channel_name)
# PkFltM3Sci_df = pd.DataFrame(columns=channel_name)
# PQube3_df = pd.DataFrame(columns=channel_name)
PkFltM1Ant_df = pd.DataFrame()
PkFltM2Tel_df = pd.DataFrame()
PkFltM3Sci_df = pd.DataFrame()
PQube3_df = pd.DataFrame()

path_data = '/Volumes/GoogleDrive/My Drive/ACEP/Data/2018/07/01' #New name format
os.chdir(path_data)
for dirpath, dirnames, files in os.walk('.', topdown=False):
    for filename in files:
        if filename.lower().endswith('.nc'):
            [meter, channel] = extract_ppty(filename, meter_name)
            if meter == meter_name[0]:
                channel_values = extract_data(dirpath, filename)
                channel_values.columns = [channel]
                PkFltM1Ant_df = pd.concat([PkFltM1Ant_df, channel_values], axis=1)
            elif meter == meter_name[1]:
                channel_values = extract_data(dirpath, filename)
                channel_values.columns = [channel]
                PkFltM2Tel_df = pd.concat([PkFltM2Tel_df, channel_values], axis=1)
            elif meter == meter_name[2]:
                channel_values = extract_data(dirpath, filename)
                channel_values.columns = [channel]
                PkFltM3Sci_df = pd.concat([PkFltM3Sci_df, channel_values], axis=1)
                # pdb.set_trace()
            elif meter == meter_name[3]:
                channel_values = extract_data(dirpath, filename)
                channel_values.columns = [channel]
                PQube3_df = pd.concat([PQube3_df, channel_values], axis=1)

# %% Save files to csv so as not to run code all the time
path_data = '/Volumes/GoogleDrive/My Drive/ACEP/Combined_data' #New name format
os.chdir(path_data)
PkFltM1Ant_df.to_csv('PkFltM1Ant_df.csv')
PkFltM2Tel_df.to_csv('PkFltM2Tel_df.csv')
PkFltM3Sci_df.to_csv('PkFltM3Sci_df.csv')
PQube3_df.to_csv('PQube3_df.csv')
# %% Data Filling

# %% Data Aggregation to a 1 minute time scale
# %% rough
# path_data = '/Volumes/GoogleDrive/My Drive/ACEP/Data/2018/07/01' #New name format
# os.chdir(path_data)
# temp = 'PokerFlatResearchRange-PokerFlat-PkFltM1AntSlidingWindowRealPowerDemand3Ph@2018-07-01T081004Z@P1D@PT151F.nc'
# cdf = xr.open_dataset(os.path.join(path_data, temp))
# cdf_df = cdf.to_dataframe()