# FAN CONTROLLER
# fan_control.py
# Evangelos Ananiadis - vaggelis.a.g.m@gmail.com / eananiadis.igemthessaly@gmail.com


# ---------------------
# - - - Local Files - -
import config
from arduino_setup import write_pin

# - - - Libraries - - -
import time
import threading
# ---------------------
global active_fan, state, period

def fan_control():
    global active_fan
    active_fan = 0
    activation_msg = 1

    while (True):
        if (state == 0):
            if (activation_msg == 1):
                print("Fan System is OFF\nAll pins set to LOW", flush=True)
                activation_msg = 0

            active_fan = 0
            for i in range(8):
                write_pin(i+2, 0)
            
        elif (state == 1):
            print(f"Fan System is ON | Fan Period={period}", flush=True)

            print(f"Pin {active_fan+2} set to HIGH", flush=True)
            for i in range(8):
                write_pin(i+2, 0)
            write_pin(active_fan+2, 1)

            active_fan = active_fan + 1
            if (active_fan == 8):
                active_fan = 0
            activation_msg = 1

        else:
            print("Something Went Wrong", flush=True)
        
        time.sleep(period)
    

def update_fan_state(fan_state, fan_period):
    global state, period
    state = 0 if fan_state == 'OFF' else 1
    period = int(fan_period)

def init_fan_system():
    global active_fan, state, period
    active_fan = 0
    state = 0
    period = 1

    fan_thread = threading.Thread(target=fan_control)
    fan_thread.daemon = True
    fan_thread.start()
