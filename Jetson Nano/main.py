import nanocamera as nano
from Car import Car
from constants import *
from detection import *
import os
import time
from PIL import Image

picam2 = nano.Camera(width=cam_width, height=cam_height)
if picam2.isReady():
    print("Cam ready")
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
        img = picam2.read()
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
