### Calculate distance between GPS points 

#load packages 
library(geosphere)
library(dplyr)

#set path
setwd("/Users/meganwilliams/Documents/GitHub/Seattle_Aquarium_ROV_telemetry_and_mapping/ROV_telemetry/QGC")

# bring in cleaned primary telemetry data file
dat = read.csv("2022-08-15_09-56-00_vehicle1_cleaned.csv")

# create new data frame with Distance column. Distance is the difference in lon, lat 
    #between rows converted from degrees to meters using the 'Haversine method'
dat2 <- dat %>% mutate(dat, Distance = distHaversine(cbind(lon, lat), cbind(lag(lon), 
                                      lag(lat))))

# save csv with distance column 
write.csv(dat2, '2022-08-15_09-56-00_vehicle1_cleaned_distance.csv', row.names = FALSE)


## END distance calculation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



