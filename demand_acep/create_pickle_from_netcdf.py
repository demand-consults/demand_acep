## This file creates the pickle from netCDF files for each meter. 

from sqlalchemy import *
import pandas as pd
import os
import config # This is the configuration for deployment 

def netCDF_to_pickle(config, data_date):
    """ 
    This function inserts into the database for the data_date specified
    
    Parameters
    ----------
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
    
    data_year = data_date[-4:]
    print(data_year)
    print(config.DATA_ROOT)
    # find this path, extract data from those files, create a dataframe, and 
    # store it as pickle in the folder. 
    data_month = data_date[0:2]
    data_day = data_date[3:5]
    print(data_month)
    print(data_day)
    data_path = os.path.join(config.DATA_ROOT, data_year, data_month, data_day)
    print(data_path)
    print(config.METER_CHANNEL_DICT)
    print(config.DATA_YEARS)
    
    return 