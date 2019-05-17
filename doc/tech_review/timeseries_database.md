# Tech-review of Timeseries Database

The question of timeseries database for this project is three-pronged. 

## 1. Why use a database instead of storing data in flatfiles?

 - Using data from a database is much easier for data analysts compared to parsing flatfiles.
 - Easy to visualize the data in a database compared to the current structure. 
 - It is much more maintainable at horizontal and vertical scale (100+ channels per meter, and imagine 100 meters). 
 - We believe due the repetition of time column in all netCDF files for the same meter, when we aggregate channels in a table in a database with primary key set to timestamp of measurement, we will save space. During the course of this project, we will test this hypothesis and post results.

## 2. Why use a timeseries database instead of a regular database like MondoDB or Postgres?

Timeseries data is different compared to other data as:

 - We mostly have 'inserts' into the tables as opposed to merges and joins. 
 - The data arrives in order. 
 - Time is the primary axis (though time-intervals can be regular or irregular). 
 
 Timeseries databases (TSDB) are special class of databases designed to handle timeseries data at scale for applications like IoT, financial trading etc. It allows easy subsetting of data based on time and has support for "age-ing" out data as usually new data is more important than old data.<sup>[1](https://blog.timescale.com/what-the-heck-is-time-series-data-and-why-do-i-need-a-time-series-database-dcf3b1b18563/)</sup>
 
## 3. Why use TimescaleDB?

The field of TSDBs is fairly new but we have a more than few contenders and different sources have different winners<sup>[2](https://www.g2.com/categories/time-series-databases) [3](https://www.slant.co/topics/1690/~best-time-series-databases-and-or-data-stores#8) [4](https://medium.com/schkn/4-best-time-series-databases-to-watch-in-2019-ef1e89a72377)</sup>. From the last link we find that in 2019, the top two free, open-source contenders are InfluxDB and TimescaleDB. 
The scale tips in favor of TimescaleDB for us as: 

 - TimescaleDB uses SQL compared to SQL-like (tending towards NoSQL) syntax of InfluxDB. NoSQL is preferred if data model/schema is uncertain, but in our case, we know that the channels we are interested in measuring are likely to change very less often. 
 - TimescaleDB is an extension of PostgreSQL, so it brings along all the robustness, familiarity and ecosystem like PostGIS which can be used for GIS queries (like "power meters within 10 miles of Fairbanks"), whereas InfluxDB is part of the Influx platform and may lead to platform lock-in when trying to do other tasks like monitoring or visualization etc.
 - InfluxDB needs SSD for storage, while TimescaleDB can work with regular HDD. SSDs are preferred though not mandatory, so allows for a low-cost storage solution.
 - Free version of InfluxDB does'nt support clustering and high availability. <sup>[5](https://www.influxdata.com/products/editions/)</sup>          

While TimescaleDB is fairly new with v1.0 released in 2018 (InfluxDB released 1.0 in 2016), they have secured VC funding<sup>[6](https://techcrunch.com/2019/01/29/timescale-announces-15m-investment-and-new-enterprise-version-of-timescaledb/)</sup> and do better than InfluxDB on most benchmarks<sup>[7](https://blog.timescale.com/timescaledb-vs-influxdb-for-time-series-data-timescale-influx-sql-nosql-36489299877/)</sup>.