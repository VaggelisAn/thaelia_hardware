# IRRIGATION CONTROL
# irrigation_control.py
# Evangelos Ananiadis - vaggelis.a.g.m@gmail.com / eananiadis.igemthessaly@gmail.com

# ---------------------
# - - - Local Files - -
import config
from arduino_setup import write_pin

# - - - Libraries - - -
import time
import threading
# ---------------------

# enables arduino pins responsible for controlling irrigation
def humidity_control():
	global state
	# activation_msg is used for printing msgs only once
	activation_msg = 1
	start_mist = 0
	humidity = 0
	temp = 0
	
	while (True):
		# sensor_lock syncs irrigation control thread + hygrometer sensor thread
		if (state == 1 and config.air_humidity < GOAL_HUMIDITY):
			if (activation_msg == 1):
				print("Activating Mist.")
				activation_msg = 0
			config.board.digital[config.HUM_CONTROL_PIN].write(1)
		elif (state == 0):
			config.board.digital[config.HUM_CONTROL_PIN].write(0)
			activation_msg = 1
		time.sleep(config.SAMPLE_HUM_DELAY)

# check whether auto irrigation was enabled through the local server 
def update_hum_state(hum_state):
	global state
	
	state = 0 if hum_state == 'OFF' else 1
	if (state == 1):
		print("Automatic Mist is ON", flush=True)
	else:
		print("Automatic Mist is OFF", flush=True)
		
	return

# initiate humidity controlling thread
def init_humidity_system():
	global state
	state = 0
	
	humidity_thread = threading.Thread(target=humidity_control)
	humidity_thread.daemon = True
	humidity_thread.start()
