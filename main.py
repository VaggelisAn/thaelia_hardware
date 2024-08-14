# MAIN FILE
# main.py
# Evangelos Ananiadis - vaggelis.a.g.m@gmail.com / eananiadis.igemthessaly@gmail.com

# ---------------------
# - - - Local Files - -
import config
from arduino_setup import init_arduino
from local_server import app
from fan_control import init_fan_system
from temp_control import init_temp_system
from sensors import init_sensors

# - - - Libraries - - -
from bottle import Bottle
# ---------------------

# Threading

def main():
    config.init()    
    init_arduino()
    init_fan_system()
    init_temp_system()
    init_sensors()
    
    # Local Server
    main_app = Bottle()
    main_app.merge(app)
    main_app.run(host='localhost', port=config.LOCAL_PORT, debug=True) 

if __name__ == '__main__':
    main()
