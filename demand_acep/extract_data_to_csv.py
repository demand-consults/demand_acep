""" The functions in this file convert the netcdf files to a dataframe and then 
write them to disk using multiprocessing. So, if we have a multi-core system, the 
extraction can happen in parallel. """

import os
import pandas as pd
import numpy as np
import pdb
import datetime
import io
from daterangeparser import parse
import multiprocessing as mp
import dill

from demand_acep import extract_data
from demand_acep import extract_ppty
from demand_acep import data_resample


def extract_csv_for_date(config, data_date):
    """ 
    This function writes the data for the data_date specified to a csv on disk.
    
    Parameters
    ----------
    config : 
        `config` contains the configuration for paths etc. needed by files. As
        an argument we can change the config files for different production 
        vs test configs 
    data_date : string
        `data_date` string will be used to extract the year and the path to the
        data. It should be in the 'mm/dd/yyyy' format. 

    Returns
    -------
    int
        Description of anonymous integer return value.
    """    
    print(data_date)
    # Get the year, month and and day from date entered
    data_year = data_date[-4:]
    data_month = data_date[0:2]
    data_day = data_date[3:5]
    # Get the corresponding path in the directory to look for the data for the day
    data_path = os.path.join(config.DATA_ROOT, data_year, data_month, data_day)
    
    # Find the count of meters
    meter_count = len(config.METER_CHANNEL_DICT)

    # Dictionary to store the names of the resulting csv files
    meter_csv_names = {}
    
    # Get the down-sampling time
    sample_time = config.SAMPLE_TIME
    
    # Create a dictionary with keys are meter names and values as dataframes 
    # containing the data for the day
    meter_collection = {}
    
    for meter_name in config.METER_CHANNEL_DICT:
        # Create an empty dataframe, the columns will be created later
        meter_collection[meter_name] = pd.DataFrame()

    #print(meter_collection)
    
    # Walk through all the files in the directory for the day's data
    for dirpath, dirnames, files in os.walk(data_path, topdown=True):
        # `files` contains the names of all the files at the location
        for filename in files:
            # Get the netcdf files, these are files with `.nc` extension
            if filename.lower().endswith('.nc'):
                # For the particular file, find out the corresponding meter and channel 
                [meter, channel] = extract_ppty(filename, config.METER_CHANNEL_DICT.keys())
                # Form the resulting csv name from the meter name
                # They are of the type - meter_name@Timestamp@Duration@Frequency
                # For e.g.: PQube3@2017-11-01T080002Z@PT23H@PT227F.cs
                meter_csv_names[meter] = '@'.join([meter, '@'.join(filename.split('@')[1:4])])[:-3] + '.csv'
                # Get the full path of the csv
                csv_name = os.path.join(data_path, meter_csv_names[meter])
                # Only extract if not already extracted to csv
                if (not os.path.isfile(csv_name)):
                    # Get the dataframe containing time and channel values
                    channel_df = extract_data(dirpath, filename)
                    # Give the dataframe column a name
                    channel_df.columns = [channel]
                    # Down-sample the data to the sampling time intended
                    channel_resampled = data_resample(channel_df, sample_time)
                    # If our meter dataframe is empty so far, i.e. if this is the 
                    # first channel being entered, then create a copy of the 
                    # resampled dataframe
                    if meter_collection[meter].empty:
                        meter_collection[meter] = channel_resampled.copy()
                    ####################### 
                    # This `else` clause handles two cases:
                    # 1. If the dataframe is not empty, then add other columns to
                    #    the dataframe. (the else case)
                    # 2. Some days have data downloaded more than once, this means 
                    #    that channels can occur more than once. (like 05/21/2018)
                    #######################
                    else:
                        # If the channel already exists in the dataframe
                        # then either the other file has updated data or 
                        # subsequent data. 
                        if channel in meter_collection[meter].columns:
                            # Get index from total dataframe 
                            idx_1 = meter_collection[meter].index
                            # Get index from file dataframe
                            idx_2 = channel_resampled.index
                            # Compare the two, if the index is contained within,
                            # then **update** the channel's value for file's indices. 
                            if np.all(np.isin(idx_2, idx_1)):
                                meter_collection[meter][channel].loc[idx_2] = channel_resampled.values.tolist()
                            # If the index is not contained, append the file df to
                            # the total dataframe
                            else:
                                meter_collection[meter] = meter_collection[meter].append(channel_resampled, sort=False)
                                meter_collection[meter].sort_index(inplace=True)
                                meter_collection[meter] = data_resample(meter_collection[meter], sample_time)
                        # If the channel does not already exist, then add the
                        # file dataframe to the total df. 
                        else:
                            meter_collection[meter] = meter_collection[meter].join(channel_resampled, how='outer')
                
    # Set the data imputation parameters
    interp_method = config.INTERP_METHOD
    interp_order = config.INTERP_ORDER
    
    # Perform the interpolation
    for meter in meter_collection:
        meter_collection[meter] = meter_collection[meter].interpolate(method=interp_method, order=interp_order)

    # Write the total dataframes to csv file
    for meter in meter_collection:
        # Convert time to the right data type
        # meter_collection[meter]['time'] = pd.to_datetime(meter_collection[meter]['time'])
        csv_name = os.path.join(data_path, meter_csv_names[meter])
        print(csv_name)
        # Only write csv if it does not exist yet
        if(not os.path.isfile(csv_name)):
            meter_collection[meter].to_csv(csv_name, header=False)

    return meter_csv_names

def printResult(result):
    print(result)
    