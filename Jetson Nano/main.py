from picamera2 import Picamera2
from Car import Car
from constants import *
from detection import *

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (cam_width, cam_height)})
picam2.configure(camera_config)
picam2.start()
car = Car()
car.default()
car.idle()
while True:
    try:
        img = picam2.capture_array()
        res = process(img)
        car.interpret(res)
    except KeyboardInterrupt:
        car.end_car()
