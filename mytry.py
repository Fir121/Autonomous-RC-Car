import cv2 
import numpy as np 
from backend import *
import time


cap = cv2.VideoCapture(1)
while True:
    success,img = cap.read()
    cv2.imshow("mainvid",img)
    outp = bw_conv(img)
    outp2 = warp_img(img)
    outp3 = bw_conv(outp2)
    cv2.imshow('wrped',outp2)
    cv2.imshow('wrpedbw',outp3)
    todo = process_direction(outp3)
    print(todo)
    cv2.waitKey(1)
'''

image = cv2.imread('asd.jpg')
cv2.namedWindow('image')
outp = bw_conv(image)
outp2 = warp_img(image)
outp3 = bw_conv(outp2)
todo = process_direction(outp3)
print(todo)
while True:
    time.sleep(0.00001)
    cv2.imshow('image',outp)
    cv2.imshow('wrped',outp2)
    cv2.imshow('wrpedbw',outp3)

    cv2.waitKey(1)

cv2.destroyAllWindows()

'''