## This module contains code for the peak demand charge analysis. All function just requires `data` input, once it is given, each function generates plots accordingly. 


# Import
library(readr)
library(dplyr)
library(tidyr)
library(ggplot2)
library(lubridate)
library(forcats)
library(pander)
library(stringr)
library(kableExtra)


# data <- read_csv(file = "../../demand_charge/data/charge_downsampled.csv") %>% mutate(time = as.Date(time, format="%m/%d/%Y"))

## This is for peak demand comparison. Input is data leading to a plot of peak demand comparison. 
peak_compare <- function(data){
  data %>% 
    ggplot(aes(x = time, y = Virtual_meter, color = "virtual meter")) +
    geom_line() +
    geom_line(aes(y = Total_4meters, color = "aggregated 4 meters"))+
    scale_color_manual(name = "Peak power (kW):", values = c("virtual meter" = "red",
                                                             "aggregated 4 meters" = "blue"))+
    scale_x_date(date_breaks = "1 month", date_labels = "%Y-%m") +
    xlab("Month (2017 - 2019)") + 
    ylab("Power (kW)") +
    ggtitle("Montly peak demand (kW)") +
    theme_bw() + 
    theme_minimal(base_size = 14) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1)) 
}

## For example, try peak_compare(data)

## This is for density comparison. Input of data will lead to a plot of two densities. 
den_compare <- function(data){
  d <- density(data$Virtual_meter, adjust = 1, na.rm = TRUE)
  d_kw <- density(data$Total_4meters, adjust = 1, na.rm = TRUE)
  plot(d, main="KDE for peak power (kW)", xlab='Power (kW)', col="red")
  lines(d_kw, col="blue")
  legend('topleft', legend=c("virtual meter", "aggregated 4 meters"),
         col=c("red", "blue"), lty=1)
}

## For example, try den_compare(data)

## This is to create a cost table including all the rates. 
cost_table <- function(data){
  
  ad_G2 = 30
  kwh_G2 = 0.06256+0.09207
  kw_G2 = 14.29
  
  ad_G3 = 295
  kwh_G3 = 0.0294+0.09207               
  kw_G3 = 22.86
  
  chrg <- data %>% 
    mutate(charge_G2= Total_4meters*kw_G2 + Tot_kwh*kwh_G2 + ad_G2*4,
           charge_G3= Virtual_meter*kw_G3 + Tot_kwh*kwh_G3 + ad_G3,
           saving = charge_G2 - charge_G3)
  
  return(chrg)
}

## For example, try chrg <- cost_table(data)

## This will show a monthly energy consumption plot for the 4 meters. 
energy_compare_plot <- function(data){
  chrg <- cost_table(data)
  plot(chrg$time, chrg$Tot_kwh/1000, main="Monthly energy consumption (MWh)", type="l", 
       xlab='Month (2017 - 2019)', col="black", ylim=c(0,400), ylab="Power consumption (MWh)", xaxt="n")
  lines(chrg$time,chrg$Wat1_e/1000, col="blue")
  lines(chrg$time,chrg$PQ_e/1000, col="red")
  lines(chrg$time,chrg$Wat3_e/1000, col="brown")
  lines(chrg$time,chrg$Wat2_e/1000, col="gold")
  axis.Date(side=1, at=chrg$time, labels=format(chrg$time, "%Y-%m"), srt = 45)
  legend('topright', legend=c("Total", "Wat1","PQ","Wat3","Wat2"),
         col=c("black","blue","red","brown","gold"), lty=1)
}


## For example, try energy_compare_plot(data)

## This shows a monthly bill plot. 
monthly_bill <- function(data){
  cost_table(data) %>% 
    ggplot(aes(x = time, y = charge_G3/ 1000, color="A virtual meter")) +
    geom_line() +
    geom_line(aes(y = charge_G2/ 1000, color="4 meters")) +
    geom_line(aes(y = saving/ 1000, color="Savings")) +
    xlab("Monthly billing cycle (2017 - 2019)") + 
    ylab("Monthly charge ($1K)") +
    theme_bw() + 
    theme_minimal(base_size = 14) +
    scale_x_date(date_breaks = "1 month", date_labels = "%Y-%m") +
    scale_color_manual(name = "Elec. Cost:", values = c("A virtual meter" = "red","4 meters" = "blue",
                                                        "Savings" = "Gold"))+
    theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
    ggtitle("Monthly electricity bill")
}

## monthly_bill(data)

## This leads to a plot of saving distribution.  
saving_distribution <- function(data){
  chrg <- cost_table(data)
  d <- density(chrg$saving/ 1000, adjust = 1, na.rm = TRUE)
  plot(d, main="KDE for savings ($1K) ", xlab='Savings ($1K)', col="red")
  abline(v=mean(chrg$saving/1000), col="blue")
  legend('topleft', legend=c("Savings", "Average savings"),
         col=c("red", "blue"), lty=1)
}

## saving_distribution(data)
