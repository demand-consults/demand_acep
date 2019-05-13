# Tech-review of NetCDF File Readers
The ACEP measurement data comes from four different meters measuring the electricity consumed and related parameters (~ 40) at different locations on the pokerflats range. These parameters from each meters are sampled multiple times per minute and stored in individual files in a format called Network Common Data Form (NetCDF). NetCDF is a file format for storing multidimensional scientific data (variables) such as temperature, humidity, pressure, wind speed, and direction <sup>[1](#myfootnote1)</sup>. 

To achieve the goal of creating a data pipeline for the measurement data, that is, accessing, reading and grouping the measurement data from the individual meters into a timeseries database, and appropriate NetCDF file reader is required. 

Three NetCDF file readers considered were:
1. NetcdfHandler.py - This is the netcdf python file received along with the dataset.
2. [netCDF4 module](https://github.com/Unidata/netcdf4-python).

3. [xarray](http://xarray.pydata.org/en/stable/why-xarray.html).

Of these NetCDF file readers, xarray was chosen as the module to be used because it:
1. Has two core data structures - DataArray and Dataset - which build upon and extend the core strengths of NumPy and pandas. 
2. Provides data structures for in-memory analytics that both utilize and preserve labels by leveraging the capabilities of Pandas.
3. Keeps a tight focus on functionality and interfaces related to labeled data, and leverages other Python libraries for everything else, e.g., NumPy/pandas for fast arrays/indexing (xarray itself contains no compiled code), Dask for parallel computing, matplotlib for plotting, etc.

With these above attributes, using xarray is easy and intuitive to use as its user-facing interfaces aim to be more explicit versions of those found in NumPy/pandas.

A list of other available tools for manipulating NetCDF files can be found [here](https://www.unidata.ucar.edu/software/netcdf/software.html).

<a name="myfootnote1">1</a>: http://help.arcgis.com/en/arcgisdesktop/10.0/pdf/netcdf-tutorial.pdf
