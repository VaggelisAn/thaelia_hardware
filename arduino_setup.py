# SETUP ARDUINO SERIAL COMMUNICATION
# arduino_setup.py
# Evangelos Ananiadis - vaggelis.a.g.m@gmail.com / eananiadis.igemthessaly@gmail.com

# ---------------------
# - - - Local Files - -
import config

# - - - Libraries - - -
import pyfirmata2
# ---------------------
PORT = pyfirmata2.Arduino.AUTODETECT

def init_arduino():
    config.board = pyfirmata2.Arduino(PORT)
    # default sampling interval of 19ms
    config.board.samplingOn()

    print("Setting up the connection to the board ...")

def write_pin(pin, state):
    if (pin < 2):
        print("Pins 0, 1 are not accessible")
    elif (pin > 13):
        print("13 Pins available")
    else:
        config.board.digital[pin].write(state)
        
