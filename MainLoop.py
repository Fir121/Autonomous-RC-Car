# THIS IS A TESTER FILE
import Car
import time

car = Car()
while True:
    print("forward")
    car.move()
    time.sleep(2)
    print("right")
    car.turn(50)
    time.sleep(2)
    print("left")
    car.turn(-50)
    time.sleep(2)
    print("full right")
    car.turn(100)
    time.sleep(2)
    print("full left")
    car.turn(-100)
    time.sleep(2)
    print("straight")
    car.turn(0)
    time.sleep(2)
    print("brake")
    car.brake()
    time.sleep(2)
    print("idle")
    car.default()
    time.sleep(2)
    break

car.end_car()