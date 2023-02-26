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
if os.path.exists("test.jpg"):
    os.remove("test.jpg")
while True:
    try:
        img = picam2.capture_array()
        if os.path.exists("op.txt"):
            os.remove("op.txt")
        cv2.imwrite("test.jpg", img)
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
        print(i)
        car.interpret(res)
        car.brake()
        time.sleep(1.5)
        if logging and img is not None:
            with open(tfile,"a+") as f:
                print("\n".join([str(i),str(res),"-----"]))
                f.writelines([str(i)+"\n",str(res)+"\n","-----\n"])
        i += 1
    except KeyboardInterrupt:
        car.end_car()
        break
    except Exception as e:
        print(e)
        car.end_car()
        break
