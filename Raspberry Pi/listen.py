from Car import Car
import serial
from serial_communicator import *
import picamera2

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (cam_width, cam_height)})
picam2.configure(camera_config)
picam2.start()

print("Opening communique")
ser = SerialCommunicator()
print("starting car")
car = Car()
while True:
    time.sleep(0.00001)
    data = ser.receive()
    data = data.split(":")

    if data[0] == "servo":
        car.turn(float(data[1]))
        
    elif data[0] == "esc":
        if data[1] == "x":
            car.default()
        if data[1] == "1":
            car.move()
        elif data[1] == "-1":
            car.brake()
        elif data[1] == "0":
            car.idle()

    elif data[0] == "car":
        if data[1] == "end":
            car.end_car()
        
    elif data[0] == "img":
        img = picam2.capture_array()
        ser.sender(img.tostring())


    elif data[0] == "INITCONN":
        car = Car()
        ser.sender("DONE")
