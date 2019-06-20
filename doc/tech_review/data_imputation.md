# Tech-review of Data Imputation Packages
After reading the ACEP measurement data into a timeseries database, the next step will be filling in missing or corrupted data in a process known as data imputation. Various python imputation modules exists and the following were considered:

1. [Sklearn Imputer](https://sklearn.org/modules/generated/sklearn.preprocessing.Imputer.html)
2. [Impyute](https://pypi.org/project/impyute/)
3. [Scipy Interpolation](https://docs.scipy.org/doc/scipy/reference/interpolate.html#univariate-interpolation)/[Pandas Interpolation](https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html)
4. [FancyImpute](https://github.com/iskandr/fancyimpute)

While these modules are useful in their own right, they were unable to handle the varying case scenarios encountered while processing the data. Ultimately, a more robust and versatile interpolation function was written to cater to the specific needs of the ACEP measurement data.


Some useful literature and articles on data imputation are:
1. Discusses general methods used for data imputation - (https://towardsdatascience.com/how-to-handle-missing-data-8646b18db0d4)
2. Discusses general methods used for data imputation using R - (https://arxiv.org/pdf/1510.03924.pdf, https://www.kaggle.com/juejuewang/handle-missing-values-in-time-series-for-beginners) 
3. Tutorial on using FancyImpute python module - (https://amueller.github.io/COMS4995-s18/slides/aml-08-021218-imputation-feature-selection/#1)
