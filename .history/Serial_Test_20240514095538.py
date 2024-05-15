import serial
import time

arduino = serial.Serial(port='COM21',   baudrate=9600, timeout=.1)


def write_read(x):
    arduino.write(bytes(x,   'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    time.sleep(0.05)
    return   data


while True:
    num = input("Enter a number: ")
    value   = write_read(num)
    print(value)
