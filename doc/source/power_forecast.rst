===================================
Power (kW) correlation and forecast
===================================

These 4 meters have power (kW) correlated each other for the past 3 years. The correlations are various depending upon the comparisons. In general, power in `PQ` meter is mostly correlated with power in `Wat3`. This founding is interesting as the more correlated, the more dependency resulting in less effective to address load reduction of having a virtual meter, are expected. Using ARIMA, power trends of each meter were forecasted based on month, which is the billing cycle for demand charge. The power trends were plotted with maximum value of the peak power during the month because the peak power decides the billing cost. For the comparison, forecasts based on day, were also plotted. The range between the upper and lower bound of forecast shows narrower than the one based on month.


.. toctree::

    correlation