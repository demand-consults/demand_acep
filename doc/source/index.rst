.. demand_acep documentation master file, created by
   sphinx-quickstart on Tue Mar 19 22:53:55 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to demand_acep's documentation!
=======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

The project `demand_acep`_
aims to make sense of the data collected by power meters at some facilities at the 
`Poker Flat Research Range`_ (PFRR) managed by `Alaska Center of Energy and Power`_ (ACEP).

About the power meters
----------------------
The data consists of 4 power meters. Three power meters are WattsOnMk2 and one 
meter is PQube. The meter names and corresponding types are listed in `meter_names.txt`_
Each meter measures around 50 channels at a sub-second resolution. The channel names 
and description can be found in `this file`_. 

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _demand_acep: https://github.com/demand-consults/demand_acep
.. _Poker Flat Research Range: http://www.pfrr.alaska.edu/content/welcome-poker-flat
.. _Alaska Center of Energy and Power: http://acep.uaf.edu/
.. _meter_names.txt: https://github.com/chintanp/demand_acep/blob/master/demand_acep/data/properties/meter_names.txt
.. _this file: https://github.com/chintanp/demand_acep/blob/master/demand_acep/data/properties/NetCDF%20Meter%20File%20Generation%20Matrix%20Copy%20Poker%20Flats.xlsx
