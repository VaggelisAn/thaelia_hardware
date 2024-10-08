# LOCAL SERVER 
# local_server.py
# Evangelos Ananiadis - vaggelis.a.g.m@gmail.com / eananiadis.igemthessaly@gmail.com

# ---------------------
# - - - Local Files - -
import config
from fan_control import update_fan_state
from temp_control import update_temp_state
from irrigation_control import update_irr_state

# - - - Libraries - - -
from bottle import Bottle, static_file, request
from os import _exit

# ---------------------

# - - - Directories & Routings - - -
ROOT_TEMPLATES = "/home/vagos/Desktop/thaelia_hardware-main/templates"

panel_filename = "panel.html"
panel_route = "/panel"

admin_filename = "admin.html"
admin_route = "/admin"

toggle_fan_route = "/toggle_fan"
toggle_temp_route = "/toggle_temperature_control"
toggle_admin_route = "/toggle_admin"
toggle_irrigation_route = "/toggle_irrigation"
close_sys_route = "/close_sys"
#------------------------------------

# Local Webserver App:
app = Bottle()

# - - Client Panel - -
# Route to serve the HTML page
@app.route(panel_route)
def panel():
    return static_file(panel_filename, ROOT_TEMPLATES)

# - - Admin Panel - -
# Route to serve the Admin Panel page
@app.route(admin_route)
def admin():
    return static_file(admin_filename, ROOT_TEMPLATES)

# Route to handle the Admin Panel AJAX request
@app.post(toggle_admin_route)
def toggle_admin(): 
    data = request.json
    pin = data['pin']
    state = data['state']
    print(f"Pin {pin} is {state}")

    if (state == "LOW"):
        config.board.digital[int(pin)].write(0)
    elif (state == "HIGH"):
        config.board.digital[int(pin)].write(1)
    else:
        print("ERROR IN BOARD STATE CHANGE")

    return "OK"
    
# Route to handle the Client Panel AJAX request
@app.post(toggle_temp_route)
def toggle_temperature(): 

    data = request.json
    temp_state = data['state']
    temp_goal = data['goalTemp']

    print("update temperature controller state")
    update_temp_state(temp_state, temp_goal)

    return "OK"



# Route to handle the Client Panel AJAX request
@app.post(toggle_fan_route)
def toggle_fan(): 

    data = request.json
    fan_state = data['state']
    fan_period = data['samplingPeriod']

    print("update fan state")
    update_fan_state(fan_state, fan_period)

    return "OK"

@app.post(toggle_irrigation_route)
def toggle_irrigation():
    data = request.json
    irr_state = data['state']
    
    print("update irrigation state")
    update_irr_state(irr_state)

    return "OK"
    
# Route to handle the Client Panel AJAX request
@app.post(close_sys_route)
def close_sys():
    
    print("Closing...")
    _exit(0)
        
    return "OK"
