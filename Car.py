import RPi.GPIO as GPIO

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

        if amt == 0:
            self.servo.ChangeDutyCycle(self.servo_controls["straight"])
        elif amt < 0:
            self.servo.ChangeDutyCycle(((abs(amt)/100) * (self.servo_controls["left"]-self.servo_controls["straight"]))+self.servo_controls["straight"])
        elif amt > 0:
            self.servo.ChangeDutyCycle(self.servo_controls["straight"] - ((abs(amt)/100) * (self.servo_controls["straight"]) - self.servo_controls["right"]))
        
        return True
    
    def move(self):
        # RN will use a fixed speed, presumes esc_controls speed > idle
        self.esc.ChangeDutyCycle(self.esc_controls["idle"]+1)
    
    def brake(self):
        # assumes reverse is brake
        self.esc.ChangeDutyCycle(self.esc_controls["reverse"])
    
    def default(self):
        self.esc.ChangeDutyCycle(self.esc_controls["idle"])
    
    def end_car(self):
        self.esc.stop()
        self.servo.stop()
        GPIO.cleanup()
    
