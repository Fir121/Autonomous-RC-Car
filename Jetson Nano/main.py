from picamera2 import Picamera2
from Car import Car
from constants import *
from detection import *
import os
import time
from PIL import Image

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (cam_width, cam_height)})
picam2.configure(camera_config)
picam2.start()
car = Car()
car.default()
car.idle()
if logging:
    st = time.time()
    dir_ = os.path.join(os.getcwd(), "outputimages", str(st))
    os.makedirs(dir_)
    tfile = os.path.join(dir_, "log.txt")

i = 0
while True:
    try:
        img = picam2.capture_array()
        res = process(img)
        car.interpret(res)
        if logging:
            im = Image.fromarray(img)
            im.save(os.path.join(dir_, f"{i}.jpeg"))
            with open(tfile,"a+") as f:
                f.writelines([str(i),str(res),"-----"])
        i += 1
    except KeyboardInterrupt:
        car.end_car()
