.. _data_pipeline:

=======================
About the data pipeline
=======================

The data pipeline comprises of three steps:

Extract 
=======

This steps takes the data from NetCDF files and creates a dataframe with time as index and values in the NetCDF file as the only column.


Transform
=========

This step takes the extracted data in the dataframe for each channel and down-samples the data to a lower resolution (1 minute default) and concatenates other channels to the dataframe keeping the same time index for each meter. The transformation step also does data imputation, i.e. fills in  the missing values. The section :ref:`data_imputation` describes the data imputation process in more details. The implementation of extraction and transformation is coupled and happens in the function `extract_csv_for_date()`_, which saves the transformed data into a csv for each year. This function also handles edge-cases like days when data download to NetCDF files happens more than once. An example extraction and transformation for a day is shown in the jupyter notebook `extract_to_csv.ipynb`_. An extraction and transformation for multiple days can be done in parallel and is shown in jupyter notebook `test_multiprocessing_csv.ipynb`_. The extraction, transformation and saving of down-sampled data to csv currently takes around 2h 10min on a 28 core, 2.4 GHz system.

Load
====

This step takes the transformed data in csv files and copies it into the timeseries database - `TimescaleDB`_. TimescaleDB `installation instructions for Ubuntu`_ are pretty straightforward and it is incredibly straightforward to use with docker, like so:

.. code-block:: bash

   sudo docker run -d -e POSTGRES_USER=<username> -e POSTGRES_PASSWORD=<password> --name <database_name> -p 5432:5432  --restart=always timescale/timescaledb

Then create a database named :code:`demand_acep` and enable the TimescaleDB extension as described in the `getting started`_ section of the TimescaleDB docs. The database schema for insertion (copy) can be created using the function `create_db_schema_from_source_files()`_ which **deletes** all the existing data and tables and creates tables for each meter for each year, with channels as columns and time as primary key. Further, "copy" operation is preferred over the "insert" since it is much faster and can be done for full resolution data too efficiently (Read `here`_ about the risks and care in using copy over insert in postgresql database). Further, a Go utility `timescaledb-parallel-copy`_ is used to copy the data to the database in parallel. The function `parallel_copy_data_for_date()`_ prepares the command for timescaledb-parallel-copy and copies the data. This command is run with the "skip-header" option to ignore the first line of each day csv file, as that date-time is repeated with the previous day. Function `parallel_copy_data_for_dates()`_ is a wrapper around the `parallel_copy_data_for_date()`_ function and does the copying for a date range. An example application of the copy operation can be seen in the jupyter notebook `timescale_parallel_copy.ipynb`_. The parallel copy takes 6min 18s on a 28 core, 2.4 GHz system.


.. _extract_csv_for_date(): https://github.com/demand-consults/demand_acep/blob/f1d08e274b4bc9506cdcf7417191f705ab0a0ce4/demand_acep/extract_data_to_csv.py#L20
.. _timescaledb-parallel-copy: https://github.com/timescale/timescaledb-parallel-copy
.. _create_db_schema_from_source_files(): https://github.com/demand-consults/demand_acep/blob/f1d08e274b4bc9506cdcf7417191f705ab0a0ce4/demand_acep/create_db_schema.py#L7
.. _extract_to_csv.ipynb: https://github.com/demand-consults/demand_acep/blob/master/scripts/extract_to_csv.ipynb
.. _test_multiprocessing_csv.ipynb: https://github.com/demand-consults/demand_acep/blob/master/scripts/test_multiprocessing_csv.ipynb
.. _parallel_copy_data_for_date(): https://github.com/demand-consults/demand_acep/blob/f1d08e274b4bc9506cdcf7417191f705ab0a0ce4/demand_acep/timescale_parallel_copy.py#L18
.. _here: https://www.postgresql.org/docs/9.4/populate.html
.. _timescale_parallel_copy.ipynb: https://github.com/demand-consults/demand_acep/blob/master/scripts/timescale_parallel_copy.ipynb
.. _parallel_copy_data_for_dates(): https://github.com/demand-consults/demand_acep/blob/f1d08e274b4bc9506cdcf7417191f705ab0a0ce4/demand_acep/timescale_parallel_copy.py#L81
.. _getting started: https://docs.timescale.com/v1.3/getting-started/setup
.. _TimescaleDB: https://www.timescale.com/
.. _installation instructions for Ubuntu: https://docs.timescale.com/v1.3/getting-started/installation/ubuntu/installation-apt-ubuntu
