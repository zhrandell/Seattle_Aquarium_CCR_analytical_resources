# Overview of data streams

## ROV derived data streams

### 23MP photo stills via GoPro HERO10
* use [CoralNet](https://coralnet.ucsd.edu/) to analyze percent-cover of aggregate species from photos. 
* NOTE that I am uncertain whether we want to use photos, OR simply extract stills from our video. Thus far it appears that video from the GoPro is better able to adapt to the variable lighting, etc., we encounter underwater . . . I'm thus inclined to prioritize extracting high quality still (see below) from video. 

### 4K 30FPS wide angle video
* VIAME
* extract stills from video. This type of task is overwhelmingly achieved in Python instead of *R*, with examples [here](https://www.geeksforgeeks.org/extract-images-from-video-in-python/), [here](https://www.codespeedy.com/extract-images-from-a-video-in-python/), [here](https://www.askpython.com/python/examples/extract-images-from-video), [here](https://www.thepythoncode.com/article/extract-frames-from-videos-in-python), and [here](https://stackoverflow.com/questions/10225403/how-can-i-extract-a-good-quality-jpeg-image-from-a-video-file-with-ffmpeg)
* photogrammetry from stills (a "down the road" objective). We can use various programs (e.g., [Agisoft](https://www.agisoft.com/)) to create mossaics of our benthic surveys. 

### ROV telemetry log
* Ping1D altitude data: see [this](https://discuss.bluerobotics.com/t/retrieve-ping-sonar-data-for-analysis/11795/7) BlueRobotics forum post for relevant information, inclduing information about photogrammetry methods. What "Lea Katz" describes is very similar to what we want to do. Also see [this](https://github.com/ES-Alexander/data-alignment) repo for python code aligning ROV imagery with Ping1D data. 
* depth: very easy to work with (see [this](https://github.com/zhrandell/Seattle_Aquarium_ROV_telemetry_and_mapping/blob/main/code/tracklog_cleaning.R) *R* script). Once we have a reliable pipeline to extract the Ping1D data, it may be interesting to combine the Ping1D altitude data with depth in order to give us a nice visual of the ROV's position / flight profile relative to the contours of the underlying seafloor. 
* GPS data: see [Issue #2](https://github.com/zhrandell/Seattle_Aquarium_ROV_telemetry_and_mapping/issues/2) for more detailed information regarding working with GPS data. 

## Satellite / aerial imagery
* DNR data for kelp canopy 

## Base layers
* Bathymetry data for Puget Sound
* Bathymetry data for the Western Strait
