try:
    from Car import Car
except:
    pass
import math
import time
import cv2
from backend import *
import time
from picamera2 import Picamera2
from constants import *
import RPi.GPIO as GPIO
from gpiozero import DistanceSensor

GPIO.setmode(GPIO.BCM)

# USE MYTRY.PY TO ADJUST YOURSELF WITHIN THE LANE, HAVE PARAMETERS TO BE TWEAKED FOR MAIN TRACK. LATER MAKE PARAMS CENTRAL AND DUALS

try:
    car = Car()
except Exception as e:
    print(e)
car.idle()


print((math.degrees(math.atan(W/map_radius))/max_steer)*100)
car.turn((math.degrees(math.atan(W/map_radius))/max_steer)*100)
car.move()

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (cam_width, cam_height)})
picam2.configure(camera_config)
picam2.start()
i = 0
sensor = DistanceSensor(echo=ECHO, trigger=TRIG)
while True:
    try:
        if sensor.distance <= min_dist:
            car.brake()
        img = picam2.capture_array()
        outp3 = bw_conv(img)
        outp4 = crop(outp3)
        carc = draw(outp4)
        cv2.imwrite(f"outputimages/{i}-Base.jpg", img)
        cv2.imwrite(f"outputimages/Processed{i}-{carc[1]}.jpg", carc[0])
        i+=1
        cv2.waitKey(1)
    except KeyboardInterrupt:
        car.end_car()



'''
# OTHER PATH DEPENDING ON TRAFFIC SIGNAL RECOGNITION
map_radius = 1.8
car.turn((math.degrees(math.atan(W/map_radius))/max_steer)*100)
time.sleep(4)
map_radius = 1
car.turn(-1*((math.degrees(math.atan(W/map_radius))/max_steer)*100))
time.sleep(4)
map_radius = 1.8
car.turn((math.degrees(math.atan(W/map_radius))/max_steer)*100)
time.sleep(4)
map_radius = 1.3
car.turn((math.degrees(math.atan(W/map_radius))/max_steer)*100)
'''