# LOCAL SERVER 
# local_server.py
# ---------------------
# - - - Local Files - -
import config
from fan_control import update_fan_state

# - - - Libraries - - -
from bottle import Bottle, static_file, request

# ---------------------

# - - - Directories & Routings - - -
ROOT_TEMPLATES = "GUI/templates"

panel_filename = "panel.html"
panel_route = "/panel"

admin_filename = "admin.html"
admin_route = "/admin"

toggle_fan_route = "/toggle_fan"
toggle_admin_route = '/toggle_admin'
#------------------------------------


# - - - Routes - - -
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
@app.post(toggle_fan_route)
def toggle_fan(): 

    data = request.json
    fan_state = data['state']
    fan_period = data['samplingPeriod']

    print("update fan state")
    update_fan_state(fan_state, fan_period)

    return "OK"
