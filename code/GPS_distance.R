### Calculate distance between GPS points 

#load packages 
library(geosphere)
library(dplyr)
library(measurements)

#set path
setwd("/Users/meganwilliams/Documents/GitHub/Seattle_Aquarium_ROV_telemetry_and_mapping/ROV_telemetry/QGC")

# bring in cleaned primary telemetry data file
dat = read.csv("2022-08-15_09-56-00_vehicle1_cleaned.csv")

## Haversine Distance ------------------------
# create new data frame with Distance column. Distance is the difference in lon, lat 
# between rows converted from degrees to meters using the 'Haversine method'
dat2 <- dat %>% mutate(dat, HavDIS = distHaversine(cbind(lon, lat), cbind(lag(lon), 
                                      lag(lat))))

# Euclidean Distance -----------------------
library(rgdal)

#Convert coordinates to SpatialPoint object 
cord.dec = SpatialPoints(cbind(dat$lon, -dat$lat), proj4string = CRS("+proj=longlat"))

# Transform coordinate system to UTM using EPSG:32610 - WGS 84 / UTM zone 10N
cord.UTM <- spTransform(cord.dec, CRS("+init=epsg:32610"))
head(cord.UTM)

# Calculate Euclidean distance (m) from UTM coordinates 
euclidDist <- sp::spDists(cord.UTM, longlat = FALSE, segments=TRUE)

# Append Euclidean distance values to data frame with first row as NA
dat2$EucDIS <- c(NA, euclidDist)

# save csv with Haversine and Euclidean distance columns 
write.csv(dat2, '2022-08-15_09-56-00_vehicle1_cleaned_distance.csv', row.names = FALSE)

## END distance calculation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
