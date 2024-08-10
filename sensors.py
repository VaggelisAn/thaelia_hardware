# SENSORS
# sensors.py

# ---------------------
# - - - Local Files - -
import config


# - - - Libraries - - -
import numpy as np
import matplotlib.pyplot as plt

# ---------------------

from machine import I2C, Pin, SoftI2C # Micropython
from time import sleep

# source: https://www.reddit.com/r/MicroPythonDev/comments/1d7cpyr/shtc3_sensor/
def read_shtc():
    i2c=SoftI2C(scl=Pin(17),sda=Pin(16))
    buf1=bytearray([0x7C,0xA2])
    while True:
        i2c.writeto(0x70,buf1)
        buf2=bytearray([0x00,0x00,0x00,0x00,0x00,0x00])
        i2c.readfrom_into(0x70,buf2)
        tempC=(buf2[1]|(buf2[0]<<8))*175/65536-45
        tempF=(tempC*1.8)+32
        humid=(buf2[4]|(buf2[3]<<8))*100/65536
        print('Temperature:',tempC,'C')
        print('Temperature:',tempF,'F')
        print('Humidity:',humid,'%')
        sleep(5)