# IRRIGATION CONTROLLER
# irrigation_control.py
# Evangelos Ananiadis - vaggelis.a.g.m@gmail.com / eananiadis.igemthessaly@gmail.com

# ---------------------
# - - - Local Files - -
import config
from arduino_setup import write_pin
from sensors import read_hygrometers

# - - - Libraries - - -
import time
import threading
# ---------------------

# enables arduino pins responsible for controlling irrigation
def irrigation_control():
	global state
	# activation_msg is used for printing msgs only once
	activation_msg = 1
	start_irrigation = 0
	
	while (True):
		start_irrigation = read_hygrometers()
		# sensor_lock syncs irrigation control thread + hygrometer sensor thread
		if (state == 1 and start_irrigation == 1):
			if (activation_msg == 1):
				print("Activating Irrigation.")
				activation_msg = 0
			config.board.digital[config.IRR_CONTROL_PIN].write(1)
		elif (state == 0):
			config.board.digital[config.IRR_CONTROL_PIN].write(0)
			activation_msg = 1
		time.sleep(config.SAMPLE_IRR_DELAY)

# check whether auto irrigation was enabled through the local server 
def update_irr_state(irr_state):
	global state
	
	state = 0 if irr_state == 'OFF' else 1
	if (state == 1):
		print("Automatic Irrigation is ON", flush=True)
	else:
		print("Automatic Irrigation is OFF", flush=True)
		
	return

# initiate irrigation controlling thread
def init_irrigation_system():
	global state
	state = 0
	
	irrigation_thread = threading.Thread(target=irrigation_control)
	irrigation_thread.daemon = True
	irrigation_thread.start()

