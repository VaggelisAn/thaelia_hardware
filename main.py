# MAIN FILE
# main.py

# ---------------------
# - - - Local Files - -
import config
from arduino_setup import init_arduino
from local_server import app
from fan_control import init_fan_system, fan_control

# - - - Libraries - - -
from bottle import Bottle
# ---------------------

# Threading

def main():
    config.init()    
    init_arduino()
    init_fan_system()

    # Local Server
    main_app = Bottle()
    main_app.merge(app)
    main_app.run(host='localhost', port=config.LOCAL_PORT, debug=True) 

if __name__ == '__main__':
    main()
