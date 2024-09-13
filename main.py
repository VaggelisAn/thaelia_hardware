# MAIN FILE
# main.py
# Evangelos Ananiadis - vaggelis.a.g.m@gmail.com / eananiadis.igemthessaly@gmail.com

# ---------------------
# - - - Local Files - -
import config
from local_server import app
from arduino_setup import init_arduino
from fan_control import init_fan_system
from temp_control import init_temp_system
from irrigation_control import init_irrigation_system
from humidity_control import init_humidity_system
from sensors import init_sensors

# - - - Libraries - - -
from bottle import Bottle
# ---------------------

# Threads:
# + main thread:        handles local server through bottle lib
# + fan system thread:  handles the (de/)activation of the fan system
# + temp system thread: handles the (de/)activation of the temp system
# + irrigation system thread: handles the (de/)activation of the watering system
# + humidity system thread: handles the (de/)activation of the humidity system
# + sensors thread:     handles matplots for the sensors 

def main():
    config.init()    
    init_arduino()
    init_fan_system()
    init_temp_system()
    init_sensors()
    init_irrigation_system()
    init_humidity_system()


    # Local Server
    main_app = Bottle()
    main_app.merge(app)
    main_app.run(host='localhost', port=config.LOCAL_PORT, debug=False) 

if __name__ == '__main__':
    main()
