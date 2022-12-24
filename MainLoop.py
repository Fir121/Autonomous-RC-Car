# THIS IS A TESTER FILE
import Car
import time

car = Car()
while True:
    car.move()
    time.sleep(1)
    car.turn(50)
    time.sleep(1)
    car.turn(-50)
    time.sleep(1)
    car.turn(100)
    time.sleep(1)
    car.turn(-100)
    time.sleep(1)
    car.turn(0)
    time.sleep(1)
    car.brake()
    time.sleep(1)
    car.default()
    time.sleep(1)

car.end_car()