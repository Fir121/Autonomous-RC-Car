import cv2 
import numpy as np 
from backend import *
import time


'''
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
while True:
    success,img = cap.read()
    cv2.imshow("mainvid",img)
    outp = bw_conv(img)
    outp2 = warp_img(img)
    outp3 = bw_conv(outp2)
    outp4 = crop(outp3)
    outp5 = draw(outp4)
    todo = process_direction(outp3)
    cv2.imshow('wrped',outp2)
    cv2.imshow('wrpedbw',outp3)
    cv2.imshow('cropwrpedbw',outp4)
    cv2.imshow('draw',outp5)
    print(todo)
    cv2.waitKey(1)
'''

image = cv2.imread('a1.jpg')
cv2.namedWindow('image')
print(image.shape)
outp = bw_conv(image)
outp2 = warp_img(image)
outp3 = bw_conv(outp2)
outp4 = crop(outp3)
outp5 = draw(outp4)
todo = process_direction(outp3)
print(todo)
while True:
    time.sleep(0.00001)
    cv2.imshow('image',outp)
    cv2.imshow('wrped',outp2)
    cv2.imshow('wrpedbw',outp3)
    cv2.imshow('cropwrpedbw',outp4)
    cv2.imshow('draw',outp5)

    cv2.waitKey(1)

cv2.destroyAllWindows()
