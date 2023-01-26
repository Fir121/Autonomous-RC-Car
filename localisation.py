from Car import Car
import math
import time
# USE MYTRY.PY TO ADJUST YOURSELF WITHIN THE LANE, HAVE PARAMETERS TO BE TWEAKED FOR MAIN TRACK. LATER MAKE PARAMS CENTRAL AND DUALS
map_radius = 1.3 #m
max_steer = 40 #deg
W = 0.2 #m

try:
    car = Car()
except:
    pass

car.turn((max_steer/math.degrees(math.atan(W/map_radius)))*100)
car.move()

while True:
    time.sleep(0.2)

'''
# OTHER PATH DEPENDING ON TRAFFIC SIGNAL RECOGNITION
map_radius = 1.8
car.turn((max_steer/math.degrees(math.atan(W/map_radius)))*100)
time.sleep(4)
map_radius = 1
car.turn(-1*((max_steer/math.degrees(math.atan(W/map_radius)))*100))
time.sleep(4)
map_radius = 1.8
car.turn((max_steer/math.degrees(math.atan(W/map_radius)))*100)
time.sleep(4)
map_radius = 1.3
car.turn((max_steer/math.degrees(math.atan(W/map_radius)))*100)
'''