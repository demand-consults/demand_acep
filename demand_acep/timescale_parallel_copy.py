"""
Functions in this file insert the data into the timescaledb database using the 
go utility provided by timescaledb called timescaledb-parallel-copy
"""

import os
import pandas as pd
import pdb
import datetime
import io
from daterangeparser import parse
import glob
import multiprocessing
import subprocess

from demand_acep import extract_data
from demand_acep import extract_ppty

def parallel_copy_data_for_date(config, data_date):
    """ 
    This function parallel copies the data for the data_date specified to the 
    appropriate table of TSDB.
    
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
    # Look for the pickle and file and use pandas_to_sql to insert the data 
    # into the database. 
    data_year = data_date[-4:]
    # print(data_year)
    # print(config.DATA_ROOT)
    # find this path, extract data from those files, create a dataframe, and 
    # store it as pickle in the folder. 
    data_month = data_date[0:2]
    data_day = data_date[3:5]
    data_path = os.path.join(config.DATA_ROOT, data_year, data_month, data_day)
    # print(data_path)
    # print(config.METER_CHANNEL_DICT)
    # print(config.DATA_YEARS)
    
    meter_count = len(config.METER_CHANNEL_DICT)
    # Create a list of lists of size of number of meters
    meter_collection = {}
    meter_pickle_names = {}
    # Path of the tsdb parallel copy go executable
    timescaledb_parallel_copy_path = "/gscratch/stf/demand_acep/go/src/github.com/timescale/timescaledb-parallel-copy/cmd/timescaledb-parallel-copy/timescaledb-parallel-copy"
    db_name = config.DB_NAME
    # Get the CPU count for parallelizing the process
    num_workers = multiprocessing.cpu_count()
    # Change this based on the database location and user
    connection_string = 'host=localhost user=cp84 sslmode=disable'
    
    
    for fname in glob.glob(os.path.join(data_path, '*.csv')):
        print(os.path.basename(fname))
        file_name = os.path.basename(fname)
        table_name = file_name.split('@')[0] + '_' + data_year
        parallel_copy_cmd = [timescaledb_parallel_copy_path, '--db-name', 
                            db_name, '--table', table_name, '--file', fname, 
                            '--workers', str(num_workers), '--connection', connection_string]
        print(parallel_copy_cmd)
        subprocess.run(parallel_copy_cmd)
        # for dirpath, dirnames, files in os.walk(data_path, topdown=True):
    #     # `files` contains the names of all the files at the location
    #     for filename in files:
    #         if filename.lower().endswith('.nc'):
    #             [meter, channel] = extract_ppty(filename, config.METER_CHANNEL_DICT.keys())
    #             meter_pickle_names[meter] = '@'.join([meter, '@'.join(filename.split('@')[1:4])])[:-3] + '.pkl'
    #             pickle_name = os.path.join(data_path, meter_pickle_names[meter])
    #             # Only extract if not already pickled
    #             if (not os.path.isfile(pickle_name)):
    #                 # print(meter)
    #                 [channel_time, channel_values] = extract_data(dirpath, filename)
    #                 if meter_collection[meter].empty:
    #                     # meter_collection[meter] = meter_collection[meter].append({'time': channel_time}, ignore_index=True)
    #                     # meter_collection[meter].loc[:, channel] = channel_values
    #                     meter_collection[meter]['time'] = channel_time
    #                 meter_collection[meter][channel] = channel_values
                
    # # Write to pickle
    # for meter in meter_collection:
    #     pickle_name = os.path.join(data_path, meter_pickle_names[meter])
    #     print(pickle_name)
    #     # Only write pickle if it does not exist yet
    #     if(not os.path.isfile(pickle_name)):
    #         # listToWrite = meter_collection[meter].to_dict(orient='records')
    #         with open(pickle_name, "wb") as dill_file:
    #             dill.dump(meter_collection[meter], dill_file)
    #             print("Pickle saved", pickle_name)
    return meter_pickle_names

def extract_data_for_dates(config, data_date_range, processes=4):
    """ 
    This function extracts the data to disk for the data_date_range specified.
    
    Parameters
    ----------
    config : 
        `config` contains the configuration for paths etc. needed by files. As
        an argument we can change the config files for different production 
        vs test configs 
    data_date_range : string
        `data_date_range` string will be used to extract the dates in the range 
        specified. The data will be inserted for all dates in between the dates
        *including* the start and end dates.
        
        **Accepted formats:**

        This parsing routine works with date ranges and single dates, and should
        work with a wide variety of human-style string formats, including:
        
        - 27th-29th June 2010
        - 30 May to 9th Aug
        - 3rd Jan 1980 - 2nd Jan 2013
        - Wed 23 Jan - Sat 16 February 2013
        - Tuesday 29 May -> Sat 2 June 2012
        - From 27th to 29th March 1999
        - 1--9 Jul
        - 14th July 1988
        - 23rd October 7:30pm
        - From 07:30 18th Nov to 17:00 24th Nov
    processes :
        `processes` defaults to 4. This should be set to the number of cores 
        available. This will parallelize the task across the number of cores 
        using Python multiprocessing Pool. 

    Returns
    -------
    int
        Description of anonymous integer return value.
    """
    
    # Get the start and end date
    start, end = parse(data_date_range)
    # Get the list of dates within the range and convert to the format we want
    dates_in_range = pd.date_range(start, end).strftime("%m/%d/%Y")
    print(dates_in_range)
    # Create a pool for the number of processes specified
    pool = mp.Pool(processes=processes)
    
    results = [pool.apply(extract_data_for_date, args=(config, data_date)) for data_date in dates_in_range]
    
    return 
    
    