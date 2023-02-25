import cv2
import time
from picamera2 import Picamera2
from Car import Car
from constants import *
import os

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (cam_width, cam_height)})
picam2.configure(camera_config)
picam2.start()
car = Car()
car.default()
car.idle()

if logging:
    st = time.time()
    dir_ = os.path.join(os.getcwd(), "outputtext", str(st))
    os.makedirs(dir_)
    tfile = os.path.join(dir_, "log.txt")

i = 0
while True:
    try:
        img = picam2.capture_array()
        cv2.imwrite("test.jpg", img)
        if os.path.exists("op.txt"):
            os.remove("op.txt")
        while True:
            if os.path.exists("op.txt"):
                while True:
                    try:
                        with open("op.txt","r") as f:
                            res = eval(f.read())
                        break
                    except Exception as e:
                        time.sleep(0.00001)
                break
            else:
                time.sleep(0.00001)
        car.interpret(res)
        i += 1
    except:
        car.end_car()
