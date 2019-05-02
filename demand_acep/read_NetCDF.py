# %% Imports
import os
import pandas as pd
import pdb


from demand_acep import extract_data
from demand_acep import extract_ppty
# %% Paths
path = os.getcwd()
# path_ppty = os.path.join(path, 'demand_acep/data/properties')
# path_data = os.path.join(path, 'demand_acep/data/measurements')
path_ppty = os.path.join(path, 'data/properties')
path_data = os.path.join(path, 'data/measurements')
# %% Read in files containing data type
filename_ppty = 'Copy of Measured Channels PFRR.xlsx'
meter_details = pd.read_excel(os.path.join(path_ppty, filename_ppty))
# Extract channel names
channel_name = ['time'] + list(meter_details['Channels'][:48])
channel_description = list(meter_details['Desc'][:48])
channel_dict = dict(zip(channel_name, channel_description))
# Extract name of meters
meter_name = list(meter_details.columns.values)[-4:]
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

