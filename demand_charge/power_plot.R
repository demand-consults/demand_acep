# This module contains codes for the peak demand plots per day, weekday, month, and year. 

# Import
library(readr)
library(dplyr)
library(tidyr)
library(ggplot2)
library(lubridate)
library(forcats)
library(pander)
library(stringr)

## This is to convert the original csv file to a formated dataframe. 
data_plot <- function(csv_path){
  read_csv(file = csv_path) %>% 
    mutate_at(vars(c(-avr, -weekday, -index_m, -index_d)), as.factor) %>% 
    mutate(weekday = parse_factor(weekday, levels = c("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday",
                                                      "Friday", "Saturday")))
  }

## data <- data_plot("../../demand_charge/data/tidy_downsampled.csv")

## This is to plot in terms of day with respect to meter, group, color and facet. 
day_plot <- function(data, meter_name, group_name, color_name, facet_name){
  
  data %>% 
    filter(meter == meter_name) %>% 
    ggplot(aes(x = index_d, y = avr, group = !!sym(group_name), color = !!sym(color_name))) +
    geom_line() +
    xlab("15 mins in a day") + 
    ylab("Power (kW)") +
    ggtitle(paste0(meter_name, " - 15 mins demand charge power (kW)")) +
    theme_bw() + 
    facet_wrap(vars(!!sym(facet_name))) +
    theme_minimal(base_size = 14)
  }

## day_plot(data, "PQ", "month", "month", "day")


## This is to plot in terms of month  with respect to meter, group, color and facet. 
month_plot <- function(data, meter_name){
  
  data %>% 
    filter(meter == meter_name) %>% 
    ggplot(aes(x = index_m, y = avr, color = year)) +
    geom_line() +
    xlab("15 mins in a month") + 
    ylab("Power (kW)") +
    ggtitle(paste0(meter_name, " - 15 mins demand charge power (kW)")) +
    theme_bw() + 
    facet_wrap(~ month) +
    theme_minimal(base_size = 14)
  } 

## month_plot(data, "PQ")
