# THIS IS A TESTER FILE
import Car
import time
from sshkeyboard import listen_keyboard

car = Car.Car()

def press(key):
    if key == "up":
        car.move()
    elif key == "down":
        car.brake()
    elif key == "left":
        car.turn(-100)
    elif key == "right":
        car.turn(100)
    elif key == "space":
        car.idle()
    else:
        car.turn(0)
        car.default()

car.default()
car.idle()
listen_keyboard(on_press=press)

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        car.end_car()