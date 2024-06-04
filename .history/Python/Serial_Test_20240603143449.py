import serial
import time

arduino = serial.Serial(port='COM12',  baudrate=9600, timeout=.1)


def write_read(x):
    arduino.write(bytes(x,  'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return  data


while True:
    value  = arduino.readline()
    time.sleep(0.05)
    print(value)
