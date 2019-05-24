# This file handles the databse insertion
# %% Imports
from sqlalchemy import * 
import pandas as pd
import sqlalchemy
import os
import pandas as pd
import pdb
import datetime
import io
from daterangeparser import parse

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
                # print(meter)
                [channel_time, channel_values] = extract_data(dirpath, filename)
                if meter_collection[meter].empty:
                    # meter_collection[meter] = meter_collection[meter].append({'time': channel_time}, ignore_index=True)
                    # meter_collection[meter].loc[:, channel] = channel_values
                    meter_collection[meter]['time'] = channel_time
                meter_collection[meter][channel] = channel_values
    
    # Make db settings 
    connect = sql_engine.connect()
    meta = MetaData(bind=sql_engine)
    meta.reflect(bind=sql_engine)
    totalRowsInserted = 0
    # Reset the index to be the time column
    for meter in meter_collection:
        # Convert time to the right data type
        meter_collection[meter]['time'] = pd.to_datetime(meter_collection[meter]['time'])
        # The orient='records' is the key of this, it allows to align with 
        # the format mentioned in the doc to insert in bulks. This should include
        # the index column in the db as a regular column in pandas df
        listToWrite = meter_collection[meter].to_dict(orient='records')
        print("Generated insert dict")
        # Get the handle of corresponding table in the metadata - assumes
        # that the table already exists
        table = meta.tables[meter + "_" + str(data_year)]
        insrt_stmnt = sqlalchemy.dialects.postgresql.insert(table).values(listToWrite)
        # Postgres upsert statement, ensuring idempotency of insert statements
        #insrt_do_nothing_stmt  = insrt_stmnt.on_conflict_do_nothing(index_elements=['time'])    
        # Execute the insert
        results = sql_engine.execute(insrt_stmnt)
        # Get number of rows inserted
        rowcount = results.rowcount
        totalRowsInserted = totalRowsInserted + rowcount
        print(rowcount)
        
    return totalRowsInserted
    
def insert_data_multiple_dates(sql_engine, config, data_date_range):
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

    Returns
    -------
    int
        Description of anonymous integer return value.
    """
    
    # Get the start and end date
    start, end = parse(data_date_range)
    # Get the list of dates within the range and convert to the format we want
    dates_in_range = pd.date_range(start, end).strftime("%m/%d/%Y")
    
    # Perform the insert for the said days
    for date in dates_in_range:
        total_row_count = insert_into_database(sql_engine, config, date)
    
    
    return total_row_count