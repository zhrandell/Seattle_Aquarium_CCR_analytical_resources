setwd(here::here())

#load libraries
library(tidyverse)
library(ggplot2)

#set paths and read in main telemetry file and Ping file from same transect 

main = read.csv("./ROV_telemetry/QGC/2022-08-15_09-56-00_vehicle1_cleaned_distance.csv")
Ping = read.csv("./ROV_telemetry/Ping/20220815-095728695_Avg_Ping.csv")

#drop unnecessary X column
main <- subset(main, select = -X)

#Merge data frames together based on time 
dat4 <- merge(main, Ping, by.x = "time")


