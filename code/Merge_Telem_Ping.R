#load libraries
library(tidyverse)
library(ggplot2)

#set paths and read in main telemetry file and Ping file from same transect 

setwd('/Users/meganwilliams/Documents/GitHub/Seattle_Aquarium_ROV_telemetry_and_mapping/ROV_telemetry/QGC')
main = read.csv("2022-08-15_09-56-00_vehicle1_cleaned_distance.csv")


setwd('/Users/meganwilliams/Documents/GitHub/Seattle_Aquarium_ROV_telemetry_and_mapping/ROV_telemetry/Ping')
Ping = read.csv("20220815-095728695_Avg_Ping.csv")

#drop unnecessary X column
main <- subset(main, select = -X)

#Merge data frames together, drop rows with NA values

dat4 <- merge(main, Ping, all=FALSE)


