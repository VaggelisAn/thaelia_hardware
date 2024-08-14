# CONFIGURATION FILE
# config.py
# Evangelos Ananiadis - vaggelis.a.g.m@gmail.com / eananiadis.igemthessaly@gmail.com

import threading

# Declare Global Variables:
def init():
    # Arduino Setup variables:
    global board
    global ARDUINO_PORT
    ARDUINO_PORT = 'COM3'

    # Local Server:
    global LOCAL_PORT
    LOCAL_PORT = 8080
    
    # Temperature Controller:
    global TEMP_CONTROL_PIN, GOAL_TEMP, TEMP_THRESH, SAMPLE_TEMP_DELAY
    TEMP_CONTROL_PIN = 10
    GOAL_TEMP = 40
    TEMP_THRESH = 2
    SAMPLE_TEMP_DELAY = 1
    
    # Sensor data:
    global air_temp, air_humidity, sensor_lock
    air_temp = {}
    air_humidity = {}
    sensor_lock = threading.Lock()
    
    




