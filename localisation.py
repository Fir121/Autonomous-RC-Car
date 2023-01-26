try:
    from Car import Car
except:
    pass
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

car.turn((math.degrees(math.atan(W/map_radius))/max_steer)*100)
car.move()

while True:
    time.sleep(0.2)

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