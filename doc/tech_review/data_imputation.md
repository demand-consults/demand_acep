# Tech-review of Data Imputation Packages
After reading the ACEP measurement data into a timeseries database, the next step will be filling in missing or corrupted data in a process known as data imputation. Various python imputation modules exists and the following were considered:

1. [Sklearn Imputer] (https://sklearn.org/modules/generated/sklearn.preprocessing.Imputer.html)
2. [Impyute](https://pypi.org/project/impyute/)
3. [Scipy-Pandas Interpolation](https://docs.scipy.org/doc/scipy/reference/interpolate.html#univariate-interpolation, https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html)
4. [FancyImpute](https://github.com/iskandr/fancyimpute)

Of these imputation modules, impyute was chosen to be used primarily because of its ability to deal with time series data imputation. Since the ACEP dataset is a time series data, methods such as autoregressive moving averages,  moving windows and last observation carried forward will be more useful and these methods are available in the impyute module. The other modules especially the FancyImpute handles random missing data by using the mean, median, mode of the data or training a regression model or a nearest neighbor model to determine the missing data. 

Some useful literature and articles on data imputation are:
1. Discusses general methods used for data imputation - (https://towardsdatascience.com/how-to-handle-missing-data-8646b18db0d4)
2. Discusses general methods used for data imputation using R - (https://arxiv.org/pdf/1510.03924.pdf, https://www.kaggle.com/juejuewang/handle-missing-values-in-time-series-for-beginners) 
3. Tutorial on using FancyImpute python module - (https://amueller.github.io/COMS4995-s18/slides/aml-08-021218-imputation-feature-selection/#1)