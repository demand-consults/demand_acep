# ACEP Demand Charge Reduction at Poker Flats Research Range (PFRR)
## 0. Data sharing and code sharing policy 
**Data sharing:** Since ACEP has spent lot of resources in collecting this data, they do not want to open it yet without ascertaining its value. The team will come up with a plan to effectively share data among the participants for research work with strict policies to not share it outside without permission from ACEP. Further, a subset of data can be used in the repository for demonstration, testing etc. and this subset will be extracted with approval from ACEP. 

**Code Sharing:** The code can be open-source or closed-source, ACEP does not plan to control this. The team will therefore continue with MIT-License open-source repo on github. (Repo link: https://github.com/demand-consults/demand_acep )

## 1. Data Pipeline
- **Data Aggregation:** Read/Load NetCDF files containing all measurements from the meters into a database.
    * [Tech review](./tech_review/timeseries_database.md) of the appropriate time-series database.
    * [Tech review](./tech_review/netcdf_reader.md) of appropriate NetCDF file reader.
    * Perform database design and data structuring.
    * Use selected NetCDF file reader to read files according to meter and measurement type
    * Export data into structured database
- **Data Filling:** Missing time series data imputation
    * [Tech review](./tech_review/data_imputation.md) of time series data imputation techniques.
    * Update missing data values using selected technique from above.
- **Anomaly Detection:** Find out if some data was recorded in error or doesn't make sense. This could be due to error in sensor reading, or transmission error or recording error. 
    * Tech review of anomaly detection mechanisms. 
    * Create separate table with anomalies. 
    * Perform remedial action on the main data. 
- **Containerization:** Discuss with ACEP team and choose an appropriate containerization tool, so that the configuration and system setup can be replicated on any machine with ease. 
    * Perform tech review of containerization technologies 
    * Test and send data pipeline container.

## 2. Forecasting
- **Data smoothing(down-sampling):** Find the appropriate time-interval for data smoothing.
    * Tech review of data smoothing techniques.
    * Understand GVEA pricing strategy. This can affect the smoothing technique/interval.
    * Perform the smoothing and create new tables.
- **Forecasting:** Using the historical data, forecast load, i.e. power and energy requirements.
    * Find appropriate forecasting horizon, should we predict for one hour in future, one day etc.
    * Perform tech review of appropriate forecasting algorithm.
    * Choose the relevant features from data for forecasting, including type of event at PFRR. 
    * Perform forecasting and generate diagnostic stats.
    
## 3. Finding solar and wind energy potential
PFRR has significant wind and solar energy generation potential. Based on the past weather data (what weather source should be used for this, get confirmation from Heike/George ), wind and solar energy generation potential can be estimated for the PFRR. 

## 4. Estimating cost savings using a virtual meter
Using the solar+wind estimates, and considering a lithium-ion ESS, create a load-leveling plan that minimizes demand charges and verify economic feasibility. This might involve using HOMER like in this paper or not like here.