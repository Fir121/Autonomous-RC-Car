import RPi.GPIO as GPIO
from constants import *

GPIO.setmode(GPIO.BCM)

class Car:
    def __init__(self, frequency=50, esc_controls={"reverse":5, "idle":7.5, "forward":10}, servo_controls={"right":5.675, "straight":7.75, "left":9.7}, esc_pin=12, servo_pin=13):
        self.frequency = frequency # Hz

        # Experimental Duty Cycle values for PWM input (in %age)
        self.esc_controls = esc_controls # This controls the speed
        self.servo_controls = servo_controls # This controls the steering

        # Pin number for esc and servo as per RPi board
        self.esc_pin = esc_pin
        self.servo_pin = servo_pin

        # Instantiates GPIO Pins to output a PWM signal
        self.esc, self.servo = self.__setup()

        # Keeps a dict of current car status
        self.status = {"esc":0, "servo":0}

        # Starts outputting a PWM signal
        self.esc.start(esc_controls["idle"])
        self.servo.start(servo_controls["straight"])
    
    def __setup(self):
        GPIO.setup(self.esc_pin, GPIO.OUT)
        GPIO.setup(self.servo_pin, GPIO.OUT)

        return GPIO.PWM(self.esc_pin, self.frequency), GPIO.PWM(self.servo_pin, self.frequency)

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
            self.servo.ChangeDutyCycle(self.servo_controls["straight"])
        elif amt < 0:
            self.servo.ChangeDutyCycle(self.servo_controls["straight"]+((self.servo_controls["left"]-self.servo_controls["straight"])*(abs(amt)/100)))
        elif amt > 0:
            self.servo.ChangeDutyCycle(self.servo_controls["straight"]-((self.servo_controls["straight"]-self.servo_controls["right"])*(amt/100)))
        
        self.status["servo"] = amt

        return True
    
    def move(self):
        # RN will use a fixed speed, presumes esc_controls speed > idle
        if self.status["esc"] == 1:
            return
        self.esc.ChangeDutyCycle(self.esc_controls["idle"]+0.5)  
        self.status["esc"] = 1
    
    def brake(self):
        # assumes reverse is brake
        if self.status["esc"] == -1:
            return
        self.esc.ChangeDutyCycle(self.esc_controls["reverse"])
        self.status["esc"] = -1
    
    def default(self):
        if self.status["esc"] is None:
            return
        self.esc.ChangeDutyCycle(0)
        self.status["esc"] = None
    
    def idle(self):
        if self.status["esc"] == 0:
            return
        self.esc.ChangeDutyCycle(self.esc_controls["idle"])
        self.status["esc"] = 0
    
    def end_car(self):
        self.esc.stop()
        self.servo.stop()
        GPIO.cleanup()
        self.status = None

    def interpret(self, control):
        if control is None:
            if self.status["esc"] == 0 or self.status["esc"] is None:
                pass
            elif self.status["esc"] == -1:
                self.default()
            else:
                self.brake()
            
            return
        
        if control < 1*0.5*0.1*cam_width and control > -1*0.5*0.1*cam_width:
            self.turn(0)
        else:
            self.turn(control/(cam_width//2)*100)
            
        self.move()
        
    
