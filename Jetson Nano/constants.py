# SOFTWARE CONSTANTS
map_radius = 4.5 #m # very variant method heavily depends on starting location, possible fix would be to computerly calculate starting location
swerve_dist = 30 # percent
min_dist = 100 #cm for sensors
max_factor = 2.6 # multiply into swerve, ensure swerve_dist*max_factor<100
acceptable_offset = 0.08 # percent/100 side to side allowed lane offset behaviour, must be <=0.5
logging = True

# HARDWARE CONSTANTS
cam_width = 640
cam_height = 480
max_steer = 40 #deg
W = 0.2 #m
TRIG_CENTER = 21
ECHO_CENTER = 22
TRIG_RIGHT = 23
ECHO_RIGHT = 24
TRIG_LEFT = 15
ECHO_LEFT = 16




