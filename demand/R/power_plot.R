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

#' data_plot
#'
#' This is to convert the original csv file to a formatted dataframe.
#' @param csv_path Input a path leading to a csv file.
#' @keywords data clean
#' @export
#' @examples
#' data_plot("./data/tidy_downsampled.csv")

data_plot <- function(csv_path){
  read_csv(file = csv_path) %>%
    mutate_at(vars(c(-avr, -weekday, -index_m, -index_d)), as.factor) %>%
    mutate(weekday = parse_factor(weekday, levels = c("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday",
                                                      "Friday", "Saturday")))
  }

## data <- data_plot("../../demand_charge/data/tidy_downsampled.csv")

#' day_plot
#'
#' This is to plot in terms of day with respect to meter, group, color and facet.
#' @param data A dataframe which has peak power values of a virtual meter and the total 4 meters.
#' @param meter_name The name of a meter
#' @param group_name The name of variable for grouping to connect plot lines.
#' @param color_name The name of variable for the same group of color.
#' @param facet_name The name of variable to split.
#' @keywords daily plot
#' @export
#' @examples
#' day_plot(data, "PQ", "month", "month", "day")

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

#' month_plot
#'
#' This is to plot in terms of month with respect to meter, group, color and facet.
#' @param data A dataframe which has peak power values of a virtual meter and the total 4 meters.
#' @param meter_name The name of a meter
#' @keywords monthly plot
#' @export
#' @examples
#' month_plot(data, "PQ")

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
