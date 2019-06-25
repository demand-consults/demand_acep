## This module contains codes for the peak demand forecast and correlation analyses.


# Import
library(readr)
library(dplyr)
library(tidyr)
library(ggplot2)
library(lubridate)
library(forcats)
library(stringr)
library(kableExtra)
library('quantmod')
library(corrplot)
library(broom)
library(forecast)

#' cor_reg
#'
#' This shows a correlation plot and spits out formatted data and a regression model with respect to PQ.
#' @param data Input a dataframe which has peak power values of a virtual meter and the total 4 meters.
#' @keywords correlation
#' @keywords regression
#' @export
#' @examples
#' cor_reg("./data/15m_downsampled.csv")

cor_reg <- function(data){
  data <- xts::xts(read_csv(file = data)[,-1], order.by = read_csv(file = data)$time)

  PQ = as.vector(data[,"PQ"])
  Wat1 = as.vector(data[,"Wat1"])
  Wat2 = as.vector(data[,"Wat2"])
  Wat3 = as.vector(data[,"Wat3"])

  rates <- data.frame(PQ, Wat1, Wat2, Wat3)
  corrplot.mixed(cor(rates, use="pairwise.complete.obs"),upper="ellipse")

  fit <- lm(PQ ~ Wat1+Wat2+Wat3)

  return(list(data, fit))

}


## Read data
# data <- read_csv(file = "../../demand_charge/data/month_downsampled.csv")

#' peak_power
#'
#' This is for a monthly peak power trend. Inputs of data and meter, it will generate a plot.
#' @param data Input a dataframe which has peak power values of a virtual meter and the total 4 meters.
#' @param meter_name Name of a meter for plotting.
#' @keywords peak power
#' @export
#' @examples
#' peak_power(data, "PQ")

peak_power <- function(data, meter_name){
  data %>%
    ggplot(aes(x = time, y = !!sym(meter_name))) +
    geom_line(color="blue") +
    scale_x_date(date_breaks = "1 month", date_labels = "%Y-%m") +
    xlab("Month (2017 - 2019)") +
    ylab("Power (kW)") +
    ggtitle(paste0(meter_name, " - demand charge power (kW)")) +
    theme_bw() +
    theme_minimal(base_size = 14) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
}

#' den_plot
#'
#' A density plot will be plotted of a specified meter.
#' @param data Input a dataframe which has peak power values of a virtual meter and the total 4 meters.
#' @param meter_name Name of a meter for plotting.
#' @keywords density
#' @export
#' @examples
#' den_plot(data, "PQ")

den_plot <- function(data, meter_name){
  d <- density(data[[meter_name]], adjust = 1, na.rm = TRUE)
  plot(d, main=paste0("KDE for ", meter_name, " power (kW)"), xlab='Power (kW)', col="red") # simple plot

}

#' arima_month
#'
#' An ARIMA forecast model in terms of month will be plotted.
#' @param data Input a dataframe which has peak power values of a virtual meter and the total 4 meters.
#' @param meter_name Name of a meter for plotting.
#' @param end_point The last value of the ordinal month, until which the model will use to forecast the rest of months.
#' @keywords ARIMA
#' @export
#' @examples
#' arima_month(data, "PQ", 13)

arima_month <- function(data, meter_name, end_point){
  dat <- data.frame(data) %>%
    drop_na()

  fit <- auto.arima(dat[[meter_name]][1:end_point], max.p = 20, max.q = 20, max.d = 2, ic = "aic")

  plot(forecast(fit), main= paste0(meter_name, " - ARIMA forecast"), col="blue",
       xlab="Ordinal month since Nov. 2017", ylab="Power (kW)")
  lines(dat[[meter_name]], col="brown")
  axis(side=1, at=c(0:end_point + 10))
  abline(v=c(end_point + 1, end_point + 3), col='red')
  text(end_point + 2, mean(dat[[meter_name]])*1.5, "Prediction vs. Real")
}


#' arima_day
#'
#' An ARIMA forecast model in terms of day will be plotted.
#' @param data Input a dataframe which has peak power values of a virtual meter and the total 4 meters.
#' @param meter_name Name of a meter for plotting.
#' @param end_point The last value of the ordinal day, until which the model will use to forecast the rest of months.
#' @keywords ARIMA
#' @export
#' @examples
#' arima_day(data, "PQ", 404)

arima_day <- function(data, meter_name, end_point){
  dat <- data.frame(data) %>%
    drop_na()

  fit <- auto.arima(dat[[meter_name]][1:end_point], max.p = 20, max.q = 20, max.d = 2, ic = "aic")

  plot(forecast(fit), col="blue", xlab="Ordinal month since Nov. 2017", ylab="Power (kW)")
  lines(dat[[meter_name]], col="brown")
  axis(side=1, at=c(seq(0, end_point+12, by=25)))
  abline(v=c(end_point + 1, end_point + 10), col='red')
  text(end_point - 50, mean(dat[[meter_name]])*1.5, "Prediction vs. Real")
}


