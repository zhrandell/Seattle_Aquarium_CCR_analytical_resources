# Overview of data streams

## ROV derived data streams

### 23MP photo stills via GoPro HERO10
* use [CoralNet](https://coralnet.ucsd.edu/) to analyze percent-cover of aggregate species from photos. 
* NOTE that I am uncertain whether we want to use photos, OR simply extract stills from our video. Thus far it appears that video from the GoPro is better able to adapt to the variable lighting, etc., we encounter underwater . . . I'm thus inclined to prioritize extracting high quality still (see below) from video. 

### 4K 30FPS wide angle video
* VIAME
* extract stills 

### ROV telemetry log
* Ping1D altitude data: see [this](https://discuss.bluerobotics.com/t/retrieve-ping-sonar-data-for-analysis/11795/7) BlueRobotics forum post for relevant information, inclduing information about photogrammetry methods. What "Lea Katz" describes is very similar to what we want to do. 
* depth: very easy to work with (see [this](https://github.com/zhrandell/Seattle_Aquarium_ROV_telemetry_and_mapping/blob/main/code/tracklog_cleaning.R) *R* script. Once we have a reliable pipeline to extract the Ping1D data, it may be interesting to combine the Ping1D altitude data with depth in order to give us a nice visual of the ROV's position / flight profile relative to the contours of the underlying seafloor. 
* GPS 

## Satellite / aerial imagery
* DNR data for kelp canopy 

## Base layers
* Bathymetry data for Puget Sound
* Bathymetry data for the Western Strait
