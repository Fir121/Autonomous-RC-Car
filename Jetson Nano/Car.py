from constants import *
import math
import ultrasonic
from serial_communicator import *
import shape_operations
import numpy as np

class Car:
    def __init__(self):
        self.send = SerialCommunicator()
    
    def readImg(self):
        data = self.send.receive()
        return np.fromstring(data, dtype=int)

    def turn(self, amt):
        self.send.sender("servo:"+str(amt))
    
    def move(self):
        self.send.sender("esc:"+"1")
    
    def brake(self):
        self.send.sender("esc:"+"-1")
    
    def default(self):
        self.send.sender("esc:"+"x")
    
    def idle(self):
        self.send.sender("esc:"+"0")
    
    def end_car(self):
        self.send.sender("car:"+"end")
    
    def default_turning(self):
        self.turn((math.degrees(math.atan(W/map_radius))/max_steer)*100)

    def interpret(self, controls):
        object_ = controls[0]
        lane_disp = controls[1]
        unoriented_lane = controls[2] # will make use when signals are introduced

        if lane_disp is None:
            self.brake()
        else:
            if object_ is not None and shape_operations.overlap(object_["box"], 0.5):
                self.brake()
                if self.sensor("center") < min_dist or self.sensor("left") < min_dist or self.sensor("right") < min_dist:
                    self.move()
                    if lane_disp > 0.5:
                        self._swerve("left",1)
                    elif lane_disp < 0.5:
                        self._swerve("right",0) # might need a time sleep here todo
                    return

            if object_ is not None and shape_operations.overlap(object_["box"], lane_disp):
                if lane_disp > object_["box"][1]:
                    lane_disp += object_["box"][3]-object_["box"][1]
                    if lane_disp > 1:
                        lane_disp = 1
                elif lane_disp < object_["box"][3]:
                    lane_disp -= object_["box"][3]-object_["box"][1]
                    if lane_disp < 0:
                        lane_disp = 0
                        
            self.move()
            if lane_disp < 0.5-acceptable_offset:
                self._swerve("right",lane_disp)
            elif lane_disp > 0.5+acceptable_offset:
                self._swerve("left",lane_disp)
            else:
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
        return ultrasonic.ultrasonic(TRIG,ECHO)
        
    def _swerve(self, side, disp):
        if side == "left":
            perct_disp = ((disp-0.5)/0.5)*100
            fact = -1
        elif side == "right":
            perct_disp = ((0.5-disp)/0.5)*100
            fact = 1
        else:
            return

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