# %% Imports
import os
import pandas as pd
import numpy as np
import pdb


from demand_acep import extract_data
from demand_acep import extract_ppty
from demand_acep import data_resample
# %% Paths
path = os.getcwd()
# path_ppty = os.path.join(path, 'demand_acep/data/properties')
# path_data = os.path.join(path, 'demand_acep/data/measurements')
path_ppty = os.path.join(path, 'data/properties')
path_data = os.path.join(path, 'data/measurements/2018/07')
# path_data = os.path.join(path, 'data/measurements/2018/05')
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
# sample_time allows the user determine what time interval the data should be resampled at
# For 1 minute - 1T, 1 hour - 1H, 1 month - 1M, 1 Day - 1D
sample_time = '1T'

# interp_method and interp_order allows the user specify the method of interpolation and the order
interp_method = 'spline'
interp_order = 2


os.chdir(path_data)
for dirpath, dirnames, files in os.walk(path_data, topdown=True):
    for filename in files:
        if filename.lower().endswith('.nc'):
            # pdb.set_trace()
            [meter, channel] = extract_ppty(filename, meter_name)
            # pdb.set_trace()
            if meter == meter_name[0]:
                channel_df = extract_data(dirpath, filename)
                channel_df.columns = [channel]
                channel_resampled = data_resample(channel_df, sample_time)
                if PkFltM1Ant_df.empty:
                    PkFltM1Ant_df = channel_resampled.copy()
                else:
                    if channel in PkFltM1Ant_df.columns:
                        idx_1 = PkFltM1Ant_df.index
                        idx_2 = channel_resampled.index
                        if np.all(np.isin(idx_2, idx_1)):
                            PkFltM1Ant_df[channel].loc[idx_2] = np.reshape(channel_resampled.values,
                                                                           (len(channel_resampled),))
                        else:
                            PkFltM1Ant_df = PkFltM1Ant_df.append(channel_resampled, sort=False)
                            PkFltM1Ant_df.sort_index(inplace=True)
                            PkFltM1Ant_df = data_resample(PkFltM1Ant_df, sample_time)
                    else:
                        PkFltM1Ant_df = PkFltM1Ant_df.join(channel_resampled, how='outer')
            elif meter == meter_name[1]:
                channel_df = extract_data(dirpath, filename)
                channel_df.columns = [channel]
                channel_resampled = data_resample(channel_df, sample_time)
                if PkFltM2Tel_df.empty:
                    PkFltM2Tel_df = channel_resampled.copy()
                else:
                    if channel in PkFltM2Tel_df.columns:
                        idx_1 = PkFltM2Tel_df.index
                        idx_2 = channel_resampled.index
                        if np.all(np.isin(idx_2, idx_1)):
                            PkFltM2Tel_df[channel].loc[idx_2] = np.reshape(channel_resampled.values,
                                                                           (len(channel_resampled),))
                        else:
                            PkFltM2Tel_df = PkFltM2Tel_df.append(channel_resampled, sort=False)
                            PkFltM2Tel_df.sort_index(inplace=True)
                            PkFltM2Tel_df = data_resample(PkFltM2Tel_df, sample_time)
                    else:
                        PkFltM2Tel_df = PkFltM2Tel_df.join(channel_resampled, how='outer')

            elif meter == meter_name[2]:
                channel_df = extract_data(dirpath, filename)
                channel_df.columns = [channel]
                channel_resampled = data_resample(channel_df, sample_time)
                if PkFltM3Sci_df.empty:
                    PkFltM3Sci_df = channel_resampled.copy()
                else:
                    if channel in PkFltM3Sci_df.columns:
                        idx_1 = PkFltM3Sci_df.index
                        idx_2 = channel_resampled.index
                        if np.all(np.isin(idx_2, idx_1)):
                            PkFltM3Sci_df[channel].loc[idx_2] = np.reshape(channel_resampled.values,
                                                                           (len(channel_resampled), ))
                        else:
                            PkFltM3Sci_df = PkFltM3Sci_df.append(channel_resampled, sort=False)
                            PkFltM3Sci_df.sort_index(inplace=True)
                            PkFltM3Sci_df = data_resample(PkFltM3Sci_df, sample_time)
                    else:
                        PkFltM3Sci_df = PkFltM3Sci_df.join(channel_resampled, how='outer')

            elif meter == meter_name[3]:
                channel_df = extract_data(dirpath, filename)
                channel_df.columns = [channel]
                channel_resampled = data_resample(channel_df, sample_time)
                # pdb.set_trace()
                if PQube3_df.empty:
                    PQube3_df = channel_resampled.copy()
                else:
                    if channel in PQube3_df.columns:
                        idx_1 = PQube3_df.index
                        idx_2 = channel_resampled.index
                        if np.all(np.isin(idx_2, idx_1)):
                            PQube3_df[channel].loc[idx_2] = np.reshape(channel_resampled.values,
                                                                           (len(channel_resampled),))
                        else:
                            PQube3_df = PQube3_df.append(channel_resampled, sort=False)
                            PQube3_df.sort_index(inplace=True)
                            PQube3_df = data_resample(PQube3_df, sample_time)
                    else:
                        PQube3_df = PQube3_df.join(channel_resampled, how='outer')


# Interpolate to fix missing data issues
PkFltM1Ant_df = PkFltM1Ant_df.interpolate(method=interp_method, order=interp_order)
PkFltM2Tel_df = PkFltM2Tel_df.interpolate(method=interp_method, order=interp_order)
PkFltM3Sci_df = PkFltM3Sci_df.interpolate(method=interp_method, order=interp_order)
PQube3_df = PQube3_df.interpolate(method=interp_method, order=interp_order)