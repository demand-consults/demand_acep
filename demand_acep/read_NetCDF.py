# %% Imports
import os
import pandas as pd
import pdb
import xarray as xr


# %% Paths
path = os.getcwd()
path_ppty = os.path.join(path, 'demand_acep/data/properties')
path_data = os.path.join(path, 'demand_acep/data/measurements')
# %% Read in files containing data type
filename_ppty = 'Copy of Measured Channels PFRR.xlsx'
meter_details = pd.read_excel(os.path.join(path_ppty, filename_ppty))
# Extract channel names
channel_name = ['time'] + list(meter_details['Channels'][:48])
channel_description = list(meter_details['Desc'][:48])
channel_dict = dict(zip(channel_name, channel_description))
# Extract name of meters
meter_name = list(meter_details.columns.values)[-4:]
# %% Functions


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

# %% Walk through folders and read .nc files using xarray


# Create Pandas dataframe for the 4 meters
PkFltM1Ant_df = pd.DataFrame()
PkFltM2Tel_df = pd.DataFrame()
PkFltM3Sci_df = pd.DataFrame()
PQube3_df = pd.DataFrame()

os.chdir(path_data)
for dirpath, dirnames, files in os.walk(path_data, topdown=True):
    for filename in files:
        if filename.lower().endswith('.nc'):
            [meter, channel] = extract_ppty(filename, meter_name)
            # pdb.set_trace()
            if meter == meter_name[0]:
                [channel_time, channel_values] = extract_data(dirpath, filename)
                if PkFltM1Ant_df.empty:
                    PkFltM1Ant_df['time'] = channel_time
                PkFltM1Ant_df[channel] = channel_values
            elif meter == meter_name[1]:
                [channel_time, channel_values] = extract_data(dirpath, filename)
                if PkFltM2Tel_df.empty:
                    PkFltM2Tel_df['time'] = channel_time
                PkFltM2Tel_df[channel] = channel_values
            elif meter == meter_name[2]:
                [channel_time, channel_values] = extract_data(dirpath, filename)
                if PkFltM3Sci_df.empty:
                    PkFltM3Sci_df['time'] = channel_time
                PkFltM3Sci_df[channel] = channel_values
            elif meter == meter_name[3]:
                [channel_time, channel_values] = extract_data(dirpath, filename)
                if PQube3_df.empty:
                    PQube3_df['time'] = channel_time
                PQube3_df[channel] = channel_values

