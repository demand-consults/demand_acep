
# Power (kW) for demand charge correlation

These 4 meters have power (kW) correlated each other for the past 3 years. The correlations are various depending upon the comparisons. In general, power in `PQ` meter is mostly correlated with power in `Wat3`. This founding is interesting as the more correlated, the more dependency resulting in less effective to address load reduction of having a virtual meter, are expected. 

![](forecast_files/figure-html/unnamed-chunk-1-1.png)<!-- -->

# Past 3 years power trends of each meter (Nov. 2017 to Apr. 2019)

Variances of power (kW) for each meter, verify the correlations found in the previous correlation plot.

![](forecast_files/figure-html/unnamed-chunk-2-1.png)<!-- -->


A regression model for power of `PQ` shows `Wat3` is the most significant followed by `Wat2` resulting in 0.72 in adjusted R-squared. They are higly correlated. 


---------------------------------------------------------------
     &nbsp;        Estimate   Std. Error   t value   Pr(>|t|)  
----------------- ---------- ------------ --------- -----------
 **(Intercept)**    15.73       0.3751      41.94        0     

    **Wat1**       0.003926    0.001164     3.373    0.0007436 

    **Wat2**        2.018      0.01534      131.5        0     

    **Wat3**        1.339      0.005774     231.9        0     
---------------------------------------------------------------

Table: Fitting linear model: PQ ~ Wat1 + Wat2 + Wat3



# Forecast based on month

Using ARIMA, power trends of each meter were forecasted based on month, which is the billing cycle for demand charge. The power trends were plotted with maximum value of the peack power during the month because the peak power decides the billing cost. 

## PQ

![](forecast_files/figure-html/unnamed-chunk-4-1.png)<!-- -->![](forecast_files/figure-html/unnamed-chunk-4-2.png)<!-- -->![](forecast_files/figure-html/unnamed-chunk-4-3.png)<!-- -->


## Wat1

![](forecast_files/figure-html/unnamed-chunk-5-1.png)<!-- -->![](forecast_files/figure-html/unnamed-chunk-5-2.png)<!-- -->![](forecast_files/figure-html/unnamed-chunk-5-3.png)<!-- -->

## Wat2

![](forecast_files/figure-html/unnamed-chunk-6-1.png)<!-- -->![](forecast_files/figure-html/unnamed-chunk-6-2.png)<!-- -->![](forecast_files/figure-html/unnamed-chunk-6-3.png)<!-- -->

## Wat3

![](forecast_files/figure-html/unnamed-chunk-7-1.png)<!-- -->![](forecast_files/figure-html/unnamed-chunk-7-2.png)<!-- -->![](forecast_files/figure-html/unnamed-chunk-7-3.png)<!-- -->



# Forecast based on day

For the comparison, forecastes based on day, were also plotted. The range between the upper and lower bound of forecast shows narrower than the one based on month. 

## PQ

![](forecast_files/figure-html/unnamed-chunk-8-1.png)<!-- -->![](forecast_files/figure-html/unnamed-chunk-8-2.png)<!-- -->![](forecast_files/figure-html/unnamed-chunk-8-3.png)<!-- -->


## Wat1

![](forecast_files/figure-html/unnamed-chunk-9-1.png)<!-- -->![](forecast_files/figure-html/unnamed-chunk-9-2.png)<!-- -->![](forecast_files/figure-html/unnamed-chunk-9-3.png)<!-- -->

## Wat2

![](forecast_files/figure-html/unnamed-chunk-10-1.png)<!-- -->![](forecast_files/figure-html/unnamed-chunk-10-2.png)<!-- -->![](forecast_files/figure-html/unnamed-chunk-10-3.png)<!-- -->

## Wat3

![](forecast_files/figure-html/unnamed-chunk-11-1.png)<!-- -->![](forecast_files/figure-html/unnamed-chunk-11-2.png)<!-- -->![](forecast_files/figure-html/unnamed-chunk-11-3.png)<!-- -->

