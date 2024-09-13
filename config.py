# CONFIGURATION FILE
# config.py
# Evangelos Ananiadis - vaggelis.a.g.m@gmail.com / eananiadis.igemthessaly@gmail.com

import threading
import warnings

# Declare and Initiate Global Variables:
def init():
    # Arduino Setup variables:
    global board
    global ARDUINO_PORT
    ARDUINO_PORT = 'COM3'

    # Local Server:
    global LOCAL_PORT
    LOCAL_PORT = 8080
    
    # Fan Controller:
    global FAN_PIN_OFFSET # offset from pin0, for fan_pin_offset=2: 
    FAN_PIN_OFFSET = 2    # fan pin[0] = dig pin2 -> fan pin[7] = dig pin9
    
    # Temperature Controller:
    global TEMP_CONTROL_PIN, GOAL_TEMP, TEMP_THRESH, SAMPLE_TEMP_DELAY
    TEMP_CONTROL_PIN = 10
    GOAL_TEMP = 20
    TEMP_THRESH = 2
    SAMPLE_TEMP_DELAY = 1
    
    # Sensor data:
    global air_temp, air_humidity, sensor_lock, start_irrigation
    air_temp = {}
    air_humidity = {}
    sensor_lock = threading.Lock()
    start_irrigation = 0
    
    # Irrigation Control:
    global IRR_CONTROL_PIN, SAMPLE_IRR_DELAY
    IRR_CONTROL_PIN = 11 # Arduino irrigation control pin
    SAMPLE_IRR_DELAY = 60
    
    # Air Humidity Control:
    global HUM_CONTROL_PIN, GOAL_HUMIDITY, SAMPLE_HUM_DELAY
    HUM_CONTROL_PIN = 12 # Humidity control pin
    GOAL_HUMIDITY = 40
    SAMPLE_HUM_DELAY = 2
    
    # Pot Humidity:
    global HYGR_PIN_OFFSET, NUM_OF_HYGR_SENSORS
    HYGR_PIN_OFFSET = 4 # offset from GPIO 0
    NUM_OF_HYGR_SENSORS = 1 
    
    # File Writing:
    global voc_file, temp_file, air_hum_file
    voc_file = open("voc_file.txt", "a")
    temp_file = open("temp_file.txt", "a")
    air_hum_file = open("air_hum_file.txt", "a")

    # Matplot lib warns against plotting outside of main thread,
    # however our main thread runs bottle, and therefore cannot
    # be used for the plotting. 
    warnings.filterwarnings("ignore")
    




