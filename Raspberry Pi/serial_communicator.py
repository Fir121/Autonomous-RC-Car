import serial
import time

class SerialCommunicator:
    def __init__(self):
        self.serial_conn = serial.Serial("/dev/ttyS0",9600)
        time.sleep(2)
        if self.receive() == "INITCONN":
            self.sender("DONE")
        else:
            raise TimeoutError
    
    def sender(self, msg):
        self.serial_conn.write(msg+"\n")
    
    def receive(self): # blocking statment
        val = self.serial_conn.readline()         
        while not '\\n'in str(val):
            time.sleep(.001)
            temp = self.serial_conn.readline()
            if not not temp.decode():
                val = (val.decode()+temp.decode()).encode()
        val = val.decode()
        val = val.strip()
        return val