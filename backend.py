import cv2 
import numpy as np 

def bw_conv(frame):
    imgHsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    kernel_size = 5
    imgHsv = cv2.GaussianBlur(imgHsv, (kernel_size, kernel_size), 0)
    lowerWhite = np.array([0,0,135])
    upperWhite = np.array([179,255,255])
    maskWhite = cv2.inRange(imgHsv, lowerWhite, upperWhite)

    return maskWhite

def warp_img(frame):
    h,w,c = frame.shape
    points = [[0,0], [w,0], [0,h], [w,h]]
    pts1 = np.float32(points)
    pts2 = np.float32([[0,0], [w,0], [0,h], [w,h]])
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgWarp = cv2.warpPerspective(frame, matrix, (w,h))

    return imgWarp

def process_direction(frame):
    return "NA"
