# CONFIGURATION FILE
# config.py

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



