## This file creates the pickle from netCDF files for each meter. 

from sqlalchemy import *
import pandas as pd
import os
import config # This is the configuration for deployment 

def netCDF_to_pickle(data_date):
    """ 
    This function inserts into the database for the data_date specified
    
    Parameters
    ----------
    data_date : string
        `data_date` string will be used to extract the year and the path to the
        data.
    data_root_path: string
        `data_root_path` should contain the root path of the data where the 
        further directory structure for dates like year\month\day is located.

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
    
    return 