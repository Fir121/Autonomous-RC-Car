# SOFTWARE CONSTANTS
map_radius = 4 # m # very variant method heavily depends on starting location, possible fix would be to computerly calculate starting location
swerve_dist = 27 # percent
min_dist = 80 # cm for sensors
max_factor = 2.4 # multiply into swerve, ensure swerve_dist*max_factor<100
acceptable_offset = 0.075 # percent/100 side to side allowed lane offset behaviour, must be <=0.5
logging = True
swerve_sleep = 0.2

# HARDWARE CONSTANTS
cam_width = 640
cam_height = 480
max_steer = 40 #deg
W = 0.2 #m
TRIG_CENTER = 27
ECHO_CENTER = 22
TRIG_RIGHT = 10
ECHO_RIGHT = 9
TRIG_LEFT = 20
ECHO_LEFT = 21