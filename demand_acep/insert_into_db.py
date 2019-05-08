# This file handles the databse insertion

from sqlalchemy import * 
import pandas as pd

# %% Imports
import os
import pandas as pd
import pdb
import datetime
import io

from demand_acep import extract_data
from demand_acep import extract_ppty
import config # This is the configuration for deployment


def insert_into_database(sql_engine, config, data_date):
    """ 
    This function inserts into the database for the data_date specified
    
    Parameters
    ----------
    sql_engine : SQLAlchemy databse engine
        `sql_engine` should support database operation.
    config : 
        `config` contains the configuration for paths etc. needed by files. As
        an argument we can change the config files for different production 
        vs test configs 
    data_date : string
        `data_date` string will be used to extract the year and the path to the
        data.

    Returns
    -------
    int
        Description of anonymous integer return value.
    """
    
    # Look for the pickle and file and use pandas_to_sql to insert the data 
    # into the database. 
    data_year = data_date[-4:]
    print(data_year)
    print(config.DATA_ROOT)
    # find this path, extract data from those files, create a dataframe, and 
    # store it as pickle in the folder. 
    data_month = data_date[0:2]
    data_day = data_date[3:5]
    data_path = os.path.join(config.DATA_ROOT, data_year, data_month, data_day)
    print(data_path)
    print(config.METER_CHANNEL_DICT)
    print(config.DATA_YEARS)
    
    meter_count = len(config.METER_CHANNEL_DICT)
    # Create a list of lists of size of number of meters
    meter_collection = {}
    
    for meter_name in config.METER_CHANNEL_DICT:
        # Get the channels for this meter
        meter_channels = config.METER_CHANNEL_DICT[meter_name]
        # Types of columns - defaulting to float, except for time
        #columns_types = [datetime.datetime] + [Float] * (len(meter_channels) - 1)
        meter_collection[meter_name] = pd.DataFrame()
        
        # pd.read_csv(io.StringIO(""), 
        # names=meter_channels, 
        # dtype=dict(zip(meter_channels,[float]*len(meter_channels))), 
        # index_col=['time']) 
    
    print(meter_collection)
    
    for dirpath, dirnames, files in os.walk(data_path, topdown=True):
        # `files` contains the names of all the files at the location
        for filename in files:
            if filename.lower().endswith('.nc'):
                [meter, channel] = extract_ppty(filename, config.METER_CHANNEL_DICT.keys())
                print(meter)
                [channel_time, channel_values] = extract_data(dirpath, filename)
                if meter_collection[meter].empty:
                    # meter_collection[meter] = meter_collection[meter].append({'time': channel_time}, ignore_index=True)
                    # meter_collection[meter].loc[:, channel] = channel_values
                    meter_collection[meter]['time'] = channel_time
                meter_collection[meter][channel] = channel_values
        
        # Reset the index to be the time column
        for meter in meter_collection:
            meter_collection[meter]['time'] = pd.to_datetime(meter_collection[meter]['time'])
            meter_collection[meter].set_index('time', inplace=True)
            
    return meter_collection