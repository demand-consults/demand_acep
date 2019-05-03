""" This file contains functions that create the schema in the database """

from sqlalchemy import create_engine  
from sqlalchemy import Table, Column, String, MetaData
import pandas as pd
import os

def read_source_file(file_path, file_name):
    """ 
    This function reads the source file and extracts the table names and
    corresponding column names.
    
    Parameters
    ----------
    file_path : string
        `file_path` represents the relative path of the source file.
    file_name : string
        The parameter `file_name` contains the name of the file containing the 
        imformation about the meter names and channels monitored etc.
    
    Returns
    -------
    int
        Description of anonymous integer return value.
    """
    
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
    
    return channel_name, meter_name
    