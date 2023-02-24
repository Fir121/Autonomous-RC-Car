from Car import Car
from constants import *
print("Importing detection")
from detection import *
print("Imported detection")
import os
import time
from PIL import Image

print("Starting car")
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
        try:
            img = car.readImg()
            res = process(img)
            car.interpret(res)
        except Exception as e:
            print(e)
        if logging and img is not None:
            im = Image.fromarray(img)
            im.save(os.path.join(dir_, f"{i}.jpeg"))
            with open(tfile,"a+") as f:
                f.writelines([str(i),str(res),"-----"])
        i += 1
    except KeyboardInterrupt:
        car.end_car()
