# demand_acep
> Python package to implement data-pipeline to process high-resolution power meter data. 

[![Build Status](https://travis-ci.com/demand-consults/demand_acep.svg?branch=master)](https://travis-ci.com/demand-consults/demand_acep) [![Coverage Status](https://coveralls.io/repos/github/demand-consults/demand_acep/badge.svg?branch=master)](https://coveralls.io/github/demand-consults/demand_acep?branch=master) [![Documentation Status](https://readthedocs.org/projects/demand-acep/badge/?version=latest)](https://demand-acep.readthedocs.io/en/latest/?badge=latest) [![PyPI version](https://badge.fury.io/py/demand-acep.svg)](https://badge.fury.io/py/demand-acep)


## Overview 
The `demand_acep` package implements a data-pipeline. The data-pipeline performs three tasks - Extraction, Transformation and Loading (ETL). 

* **Extract**: The high-resolution (~7 Hz) power meter data for each meter and each channel is read from the NetCDF files to a pandas dataframe. 
* **Transform**: The data is down-sampled to a lower resolution (1 minute default), missing data is filled, individual channel data is combined with other channels to create a dataframe down-sampled, filled dataframe per day per meter, and this dataframe is exported to a csv file. So, we have for each day of data, a csv file for each meter containing the data for all channels at a lower resolution. 
* **Load**: All the down-sampled data is loaded (copied not inserted for speed) on to the timeseries database, TimescaleDB. The data was copied back from the database to perform the data imputation for the missing days and re-copied to create the complete data. The ETL process is summarised in the poster shown below. 

<img src="https://github.com/demand-consults/demand_acep/blob/master/doc/source/_static/demand_acep_poster_DIRECT_final.jpg" width="80%">

All or some steps can be re-used or repeated as desired. Further analysis using the complete data was performed and results have been in presented in the documentation. 


## Installation

```sh
pip install demand-acep
```
> This package has only been tested on Linux. 


## Usage example

Usage examples and further analysis can be seen in the `scripts` folder. 

*  [Extract data to csv](https://github.com/demand-consults/demand_acep/blob/master/scripts/extract_to_csv.ipynb): This file shows how to extract data for a data to csv. This read a data for a day, and performs the transformation and creates CSVs for each meter and described before. 
* [Extract data for multiple days in parallel](https://github.com/demand-consults/demand_acep/blob/master/scripts/test_multiprocessing_csv.ipynb): This file shows how to use `multi-processing` library in python to extract data for multiple days in parallel. The more cores the system has, the faster the total data can be extracted. 
* [Copy data in parallel to TimescaleDB database](https://github.com/demand-consults/demand_acep/blob/master/scripts/timescale_parallel_copy.ipynb): This jupyter notebook shows how to copy the csv files to the database in parallel. 
* [Perform data imputation for long timescales (days-months)](https://github.com/demand-consults/demand_acep/blob/master/scripts/test_large_missing_data.ipynb): This jupyter notebook shows how to perform data imputation for long timescales, essentially when the data was not downloaded for a particular day, or months. 
* [Read from database to pandas dataframe](https://github.com/demand-consults/demand_acep/blob/master/scripts/read_sql.ipynb): This jupyter notebook shows how to read the data from a postgres (TimescaleDB) database into a dataframe. 


## Test-Driven Development setup

The module supports TDD and includes setup for automatic test runner. To begin development, install [Python 3.6+](https://www.python.org/) using [Anaconda](https://www.anaconda.com/) and [NodeJS](https://nodejs.org/en/) for your platform and then do the following:

* Clone the repository on your machine using `git clone https://github.com/demand-consults/demand_acep`. This will create a copy of this repository on your machine. 
* Go to the repository folder using `cd demand_acep`. 
* Get python dependencies using `pip install -r requirements.txt`. 
* Get the required node modules using `npm install`. Install [Grunt](https://gruntjs.com/api/grunt) globally using `npm install -g grunt`. This step and Nodejs is only required for automated test running. 
* In a dedicated terminal window run `grunt` on the command line. This will watch for changes to any of the `.py` files in the `demand_acep` folder and run the tests using `pytest`. 
* Make tests for the functionality you plan to implement in the `tests` folder and add the data needed for tests to the `data` folder located in `demand_acep\data`. 


## Updating Documentation

`doc` folder contains the documentation related to the package. To make changes to the documentation, following workflow is suggested:

* From the root directory of the package, i.e. here, run `grunt doc`. This command watches for changes in the `.rst` files in the `doc` folder and runs `make html`. This has the effect of building your documenation on each save. 
* To view the changes, it is suggested to run a local webserver. This can be done by first installing a webserver with `pip install sauth`, and then running the webserver like so: `sauth <username> <password> localhost <port>` from the `doc` folder in a separate terminal window. Specify a username, password and a port number, for example - 8000. Then navigate to: [http://localhost:8000](http://localhost:8000) in your web-browser and enter the username and password you set while running `sauth`. The live changes to the documentation can be viewed by navigating to the `html` folder in the `build` directory located at `doc\build\html`. 
* As you make changes to the documentation in the `.rst` files, and re-save them, `grunt doc` automatically updates the `html` folder and changes can be viewed in the browser by refreshing it. 


## Release History

* 0.0.1
    * Released to ACEP on 06/21/2019.


## Meta

Chintan Pathak, Yohan Min, Atinuke Ademola-Idowu - cp84@uw.edu, min25@uw.edu, aidowu@uw.edu.
Distributed under the MIT license. See ``LICENSE`` for more information.


## Contributing

1. Fork it (<https://github.com/demand-consults/demand_acep/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
