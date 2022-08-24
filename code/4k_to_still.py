import cv2
import os

import sys
import argparse

def extractImages(pathIn, pathOut):
	count = 0
	vidcap = cv2.VideoCapture('//Users/meganwilliams/Documents/SEAQ/ROV_video/Centennial_park_trim.mp4')
	success,image = vidcap.read()
	success = True
	while success:
		vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000)) 
		success,image = vidcap.read()
		print('Read a new frame: ', success)
		cv2.imwrite( '/Users/meganwilliams/Documents/SEAQ/ROV_video/Centennial_stills' + "\\frame%d.jpg" % count, image)     # save frame as JPEG file
		count = count + 10 #every 10 seconds 

	    

if __name__=="__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--pathIn", help="path to video")
    a.add_argument("--pathOut", help="path to images")
    args = a.parse_args()
    print(args)
    extractImages(args.pathIn, args.pathOut)