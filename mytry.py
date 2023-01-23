import cv2 
import numpy as np 
from backend import *
import time
try:
    from Car import Car
except:
    pass
from constants import *

'''
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)
try:
    car = Car()
except:
    pass
i = 0
while True:
    success,img = cap.read()
    cv2.imshow("mainvid",img)
    outp2 = warp_img(img)
    outp3 = bw_conv(outp2)
    outp4 = crop(outp3)
    outp5,carc = draw(outp4)
    cv2.imshow('wrped',outp2)
    cv2.imshow('wrpedbw',outp3)
    cv2.imshow('cropwrpedbw',outp4)
    cv2.imshow('draw',outp5)
    cv2.imwrite(f"outputimages/{i}-Processed.jpg", outp5)
    cv2.imwrite(f"outputimages/{i}-Base.jpg", img)
    i+=1

    try:
        car.interpret(carc)
    except Exception as e:
        print(e)
        
    cv2.waitKey(1)


'''

image = cv2.imread('a99.jpg')
cv2.namedWindow('image')
print(image.shape)
outp3 = bw_conv(image)
outp4 = crop(outp3)
outp5,x = draw(outp4)
print(x)
while True:
    time.sleep(0.00001)
    cv2.imshow('wrpedbw',outp3)
    cv2.imshow('cropwrpedbw',outp4)
    cv2.imshow('draw',outp5)

    cv2.waitKey(1)

cv2.destroyAllWindows()
