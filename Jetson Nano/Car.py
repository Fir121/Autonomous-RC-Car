import pigpio
import constants
import math
import ultrasonic
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
            return False 

        if amt == self.status["servo"]:
            return True

        if amt == 0:
            self._servo_change(self.servo_controls["straight"])
        elif amt < 0:
            self._servo_change(self.servo_controls["straight"]+((self.servo_controls["left"]-self.servo_controls["straight"])*(abs(amt)/100)))
        elif amt > 0:
            self._servo_change(self.servo_controls["straight"]-((self.servo_controls["straight"]-self.servo_controls["right"])*(amt/100)))
        
        self.status["servo"] = amt

        return True
    
    def move(self):
        # RN will use a fixed speed, presumes esc_controls speed > idle
        if self.status["esc"] == 1:
            return
        self._esc_change(self.esc_controls["idle"]+0.5)  
        self.status["esc"] = 1
    
    def brake(self):
        # assumes reverse is brake
        if self.status["esc"] == -1 or self.status["esc"] == 0:
            return
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

    def interpret(self, controls):
        if len(controls) == 0:
            print("braking due to no detection")
            self.brake()
        elif controls[-1]["class_name"] == "TrackLine":
            lane = controls[-1]  
            xpos = lane["xpos"]              
            if len(controls) > 1:
                objects = controls[0:-1]
                ymax = objects[0]
                for obj in objects:
                    if obj["class_name"] != "TrackLine" and obj["ypos"] > ymax["ypos"]:
                        ymax = obj
                box_offset = ymax["xpos"]
                if box_offset > 0.5+constants.box_offset_range or box_offset < 0.5-constants.box_offset_range:
                    if box_offset < 0.5:
                        xpos += (box_offset)/2
                    elif box_offset > 0.5:
                        xpos -= (1-box_offset)/2

                self.brake()
                sr = self.sensor("center")
                print(sr)
                if sr <= constants.min_dist:
                    if box_offset < 0.5 and lane["xpos"] > box_offset:
                        self.move()
                        self._swerve("left",1)
                        self.brake()
                        return
                    elif box_offset > 0.5 and lane["xpos"] < box_offset:
                        self.move()
                        self._swerve("right",0)
                        self.brake()
                        return
                elif box_offset <= 0.5+constants.box_offset_range or box_offset >= 0.5-constants.box_offset_range:
                    if 1-constants.offset_range <= xpos:
                        self.move()
                        self._swerve("left",1)
                        self.brake()
                        return
                    elif constants.offset_range >= xpos:
                        self.move()
                        self._swerve("right",0)
                        self.brake()
                        return
                else:
                    self.move()

            if constants.offset_range >= xpos:
                self._swerve("right", xpos)
            elif 1-constants.offset_range <= xpos:
                self._swerve("left", xpos)
        else:
            print("braking due to no lane detection")
            self.brake()
        
        x = (math.degrees(math.atan(constants.W/constants.map_radius))/constants.max_steer)*100
        print(x)
        self.turn(x)
        self.move()
        '''
        flag = False
        objFlag = False
        lane = None
        obj = []
        for control in controls:
            if control["class_name"] == "Zebra":
                print("Zebra detected")
                continue
            elif control["class_name"] == "TrackLine":
                flag = True
                lane = control
                if constants.offset_range >= control["xpos"] and not objFlag:
                    self._swerve("right", control["xpos"])
                elif 1-constants.offset_range <= control["xpos"] and not objFlag:
                    self._swerve("left", control["xpos"])
            else:
                objFlag = True
                obj.append(control)

        if objFlag and flag:
            ymax = obj[0]
            for control in controls:
                if control["class_name"] != "TrackLine" and control["ypos"] > ymax["ypos"]:
                    ymax = control
            if ymax["ypos"] >= constants.ignore_y:
                print("braking")
                self.brake()
                sr = self.sensor("center")
                print("sesnor reading", sr)
                if  sr <= constants.min_dist:
                    if lane["xpos"] > 0.5:
                        self.move()
                        self._swerve("left",1)
                        #self._swerve("right",0)
                    elif lane["xpos"] < 0.5:
                        self.move()
                        self._swerve("right",0)
                        #self._swerve("left",1)
                    else:
                        self.move()
                        if constants.offset_range >= lane["xpos"]:
                            self._swerve("right", lane["xpos"])
                        elif 1-constants.offset_range <= lane["xpos"]:
                            self._swerve("left", lane["xpos"])
                        else:
                            x = (math.degrees(math.atan(constants.W/constants.map_radius))/constants.max_steer)*100
                            print(x)
                            self.turn(x)
                    return
            control = lane
            self.move()
            if constants.offset_range >= control["xpos"]:
                self._swerve("right", control["xpos"])
            elif 1-constants.offset_range <= control["xpos"]:
                self._swerve("left", control["xpos"])
            x = (math.degrees(math.atan(constants.W/constants.map_radius))/constants.max_steer)*100
            print(x)
            self.turn(x)
        elif flag:
            x = (math.degrees(math.atan(constants.W/constants.map_radius))/constants.max_steer)*100
            print(x)
            self.turn(x)
            self.move()
        else:
            print("braking due to no lane")
            self.brake()
        '''
    
    def sensor(self, side):
        TRIG = ECHO = 0
        if side == "center":
            TRIG = constants.TRIG_CENTER
            ECHO = constants.ECHO_CENTER
        elif side == "left":
            TRIG = constants.TRIG_LEFT
            ECHO = constants.ECHO_LEFT
        elif side == "right":
            TRIG = constants.TRIG_RIGHT
            ECHO = constants.ECHO_RIGHT
        else:
            return None
        return ultrasonic.ultrasonic(TRIG,ECHO)
        
    def _swerve(self, side, disp):
        if side == "left":
            print("Swerving left")
            perct_disp = ((disp-0.5)/0.5)*100
            if perct_disp < 50:
                print("<50")
                self.turn((-1*constants.swerve_dist)//2)
            elif perct_disp < 80:
                print("<80")
                self.turn(-1*constants.swerve_dist)
            elif perct_disp == 100:
                print("special 100")
                self.turn(-1*int(constants.swerve_dist*constants.max_factor))
            else:
                print(">80")
                self.turn(-1*constants.swerve_dist*2)
            time.sleep(constants.swerve_time)
        elif side == "right":
            print("Swerving right")
            self.turn(constants.swerve_dist)
            perct_disp = ((0.5-disp)/0.5)*100
            if perct_disp < 50:
                print("<50")
                self.turn((constants.swerve_dist)//2)
            elif perct_disp < 80:
                print("<80")
                self.turn(constants.swerve_dist)
            elif perct_disp == 100:
                print("special 100")
                self.turn(int(constants.swerve_dist*constants.max_factor))
            else:
                print(">80")
                self.turn(constants.swerve_dist*2)
            time.sleep(constants.swerve_time)