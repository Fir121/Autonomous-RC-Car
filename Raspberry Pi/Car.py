import pigpio
from constants import *
from Globals import *
import math
import ultrasonic
import shape_operations
import time
pi = pigpio.pi()

class Car:
    def __init__(self, frequency=50, esc_controls={"reverse":5, "idle":7.5, "forward":10}, servo_controls={"right":5.675, "straight":7.75, "left":9.7}, esc_pin=12, servo_pin=13):
        self.frequency = frequency # Hz

        # Experimental Duty Cycle values for PWM input (in %age)
        self.esc_controls = esc_controls # This controls the speed
        self.servo_controls = servo_controls # This controls the steering

        # Pin number for esc and servo as per RPi board
        self.esc_pin = esc_pin
        self.servo_pin = servo_pin

        # Keeps a dict of current car status
        self.status = {"esc":0, "servo":0}

        # Starts outputting a PWM signal
        self._esc_change(esc_controls["idle"])
        self._servo_change(servo_controls["straight"])

        self._temp_left = None
        self._temp_right = None

    def _esc_change(self, num):
        pi.hardware_PWM(self.esc_pin,self.frequency,int(num*10000))
    
    def _servo_change(self, num):
        pi.hardware_PWM(self.servo_pin,self.frequency,int(num*10000))

    def turn(self, amt):
        # -100 <-> 0 <-> +100 
        # %of turning radius 
        # L <-> S <-> R
        # Function presumes that servo_controls R < S < L
        if abs(amt) > 100:
            if amt > 0:
                amt = 100
            elif amt < 0:
                amt = -100

        if amt == self.status["servo"]:
            return True

        if amt == 0:
            self._servo_change(self.servo_controls["straight"])
        elif amt < 0:
            self._servo_change(self.servo_controls["straight"]+((self.servo_controls["left"]-self.servo_controls["straight"])*(abs(amt)/100)))
        elif amt > 0:
            self._servo_change(self.servo_controls["straight"]-((self.servo_controls["straight"]-self.servo_controls["right"])*(amt/100)))
        
        print(amt)
        self.status["servo"] = amt

        return True
    
    def move(self):
        # RN will use a fixed speed, presumes esc_controls speed > idle
        if self.status["esc"] == 1:
            return
        print("move called")
        self._esc_change(self.esc_controls["idle"]+0.5) # increase speed to murder competition
        self.status["esc"] = 1
    
    def brake(self):
        # assumes reverse is brake
        if self.status["esc"] == -1 or self.status["esc"] == 0 or self.status["esc"] is None:
            return
        print("brake called")
        self._esc_change(self.esc_controls["reverse"])
        self.status["esc"] = -1
    
    def default(self):
        if self.status["esc"] is None:
            return
        self._esc_change(0)
        self.status["esc"] = None
    
    def idle(self):
        if self.status["esc"] == 0:
            return
        self._esc_change(self.esc_controls["idle"])
        self.status["esc"] = 0
    
    def end_car(self):
        self._esc_change(0)
        self._servo_change(0)
        pi.stop()
        self.status = None
    
    def default_turning(self):
        if OUTER_TRACK:
            self.turn((math.degrees(math.atan(W/map_radius))/max_steer)*100)
        else:
            self.turn(0)

    def interpret_outer(self, controls):
        object_ = controls[0]
        lane_disp = controls[1]
        unoriented_lane = controls[2] 
        hump = controls[3]
        signal = controls[4]
        zebra = controls[5]

        if USE_INNER:
            if hump is not None:
                HUMP_SEEN = True
                print("HUMP SEEN IS SET")
            elif HUMP_SEEN and unoriented_lane is not None:
                print("unoriented")
                self.move()
                self._swerve_inner("right",0)
                HUMP_SEEN = False
                OUTER_TRACK = False
                return

        if lane_disp is None:
            if MOVE_IF_NOT_DETECTED:
                self.move()
                self.default_turning()
            else:
                print("Lane not detected")
                self.brake()
        else:
            if object_ is not None:
                self.brake()
                if self.sensor("center") < min_dist:
                    self.move()
                    if lane_disp > 0.5:
                        self._swerve_outer("left", 1)
                        if SLEEP_WHILE_SWERVE:
                            self._swerve_outer("right",0.2)
                    elif lane_disp < 0.5:
                        self._swerve_outer("right",0)
                        if SLEEP_WHILE_SWERVE:
                            self._swerve_outer("left",0.8)
                    self.default_turning()
                    return
                else:
                    if object_["class_name"] != "Cone": # assumes outer has no cones
                        if object_["ypos"] < lane_disp:
                            lane_disp += (object_["box"][3]-object_["box"][1])//1.5
                            if lane_disp > 1:
                                lane_disp = 1
                        elif object_["ypos"] > lane_disp:
                            lane_disp -= (object_["box"][3]-object_["box"][1])//1.5
                            if lane_disp < 0:
                                lane_disp = 0

            self.move()
            if lane_disp < 0.5-acceptable_offset:
                self._swerve_outer("right",lane_disp)
            elif lane_disp > 0.5+acceptable_offset:
                self._swerve_outer("left",lane_disp)
            self.default_turning()

    def interpret_inner(self, controls):
        object_ = controls[0]
        lane_disp = controls[1]
        unoriented_lane = controls[2] 
        hump = controls[3]
        signal = controls[4]
        zebra = controls[5]

        if unoriented_lane is not None:
            print("unoriented")
            self.move()
            self._swerve_inner("right",0)
            OUTER_TRACK = True
        elif lane_disp is None:
            self.move()
            self._swerve_inner("left",0.75)
        elif (hump is not None and lane_disp is None):
            self.move()
            self._swerve_inner("left", 0.9)
        else:
            if object_ is not None:
                self.brake()
                if self.sensor("center") < min_dist:
                    self.move()
                    if lane_disp > 0.5:
                        self._swerve_inner("left", 0.8)
                    elif lane_disp < 0.5:
                        self._swerve_inner("right",0.2)
                    self.default_turning()
                    return
                else:
                    if object_["class_name"] == "Cone" and shape_operations.overlap(object_["box"],lane_disp): # assumes inner has no boxes
                        if object_["ypos"] < lane_disp:
                            lane_disp += 0.1
                        elif object_["ypos"] > lane_disp:
                            lane_disp -= 0.1

            self.move()
            # not using offset here>keep in mind if debugging is needed
            if lane_disp < 0.5:
                self._swerve_inner("right",lane_disp)
            elif lane_disp > 0.5:
                self._swerve_inner("left",lane_disp)
            self.default_turning()
    
    def sensor(self, side):
        TRIG = ECHO = 0
        if side == "center":
            TRIG = TRIG_CENTER
            ECHO = ECHO_CENTER
        elif side == "left":
            TRIG = TRIG_LEFT
            ECHO = ECHO_LEFT
        elif side == "right":
            TRIG = TRIG_RIGHT
            ECHO = ECHO_RIGHT
        else:
            return None
        dist = ultrasonic.ultrasonic(TRIG,ECHO)
        print(f"Sensor {side} is {dist}")
        return dist

    def _swerve_outer(self, side, disp):
        if side == "left":
            perct_disp = ((disp-0.5)/0.5)*100
            fact = -1
        elif side == "right":
            perct_disp = ((0.5-disp)/0.5)*100
            fact = 1
        else:
            return

        print("swerve called with args: "+side+f"fact:{fact}, %:{perct_disp}")
        if perct_disp < 30:
            self.turn((fact*swerve_dist)//3)
        elif perct_disp < 50:
            self.turn((fact*swerve_dist)//2)
        elif perct_disp < 80:
            self.turn(fact*swerve_dist)
        elif perct_disp == 100: #special superswerve
            self.turn(fact*int(swerve_dist*max_factor))
        else:
            self.turn(fact*swerve_dist*2)
        if SLEEP_WHILE_SWERVE:
            time.sleep(swerve_sleep)
        
    def _swerve_inner(self, side, disp):
        if side == "left":
            perct_disp = ((disp-0.5)/0.5)*100
            fact = -1
        elif side == "right":
            perct_disp = ((0.5-disp)/0.5)*100
            fact = 1
        else:
            return

        print("swerve called with args: "+side+f"fact:{fact}, %:{perct_disp}")
        if perct_disp < 30:
            self.turn((fact*swerve_dist_inner)//2)
        elif perct_disp < 65:
            self.turn((fact*swerve_dist_inner)//1.2)
        elif perct_disp < 90:
            self.turn(fact*swerve_dist_inner)
        else:
            self.turn(fact*swerve_dist_inner*2)
        if SLEEP_WHILE_SWERVE:
            time.sleep(swerve_sleep_inner)