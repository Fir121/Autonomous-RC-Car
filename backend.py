import cv2 
import numpy as np 

def bw_conv(frame):
    imgHsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    kernel_size = 5
    imgHsv = cv2.GaussianBlur(imgHsv, (kernel_size, kernel_size), 0)
    sensitivity = 15
    lowerWhite = np.array([0,0,255-sensitivity])
    upperWhite = np.array([255,sensitivity,255])
    maskWhite = cv2.inRange(imgHsv, lowerWhite, upperWhite)

    return maskWhite

def warp_img(frame):
    h,w,c = frame.shape
    points = [[w//6,0], [w-(w//6),0], [0,h], [w,h]]
    pts1 = np.float32(points)
    pts2 = np.float32([[0,0], [w,0], [0,h], [w,h]])
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgWarp = cv2.warpPerspective(frame, matrix, (w,h))

    return imgWarp

def process_direction(frame):
    return "NA"

def crop(img):
    print(img.shape)
    return img[0:700, 0:1280]

def draw(img2):
    img = img2.copy()
    contours,hierarchy = cv2.findContours(img, 1, 2)
    
    cnt_arr = []
    i=0
    for cnt in contours:
        i+=1
        x1,y1 = cnt[0][0]

        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cnt_arr.append(box)
        print(box,i)
        cv2.drawContours(img,[box],0,(255,255,255),2)
        cv2.putText(img, f'Bounds {i}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    calc_off_center(cnt_arr)
    return img

def calc_off_center(ar):
    if len(ar) == 0:
        return None
        
    x_max = ar[0]
    for x in ar:
        if x[0][1] > x_max[0][1]:
            x_max = x
    
    center = 1280//2
    rect_center = x_max[0][1]

    skew = -1*(center-rect_center) #left negative, right positive, 0 PERFECT

    print("OC By", skew)
    