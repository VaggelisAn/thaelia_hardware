# TEMPERATURE CONTROLLER
# temp_control.py
# Evangelos Ananiadis - vaggelis.a.g.m@gmail.com / eananiadis.igemthessaly@gmail.com

# ---------------------
# - - - Local Files - -
import config
from arduino_setup import write_pin

# - - - Libraries - - -
import time
import threading
# ---------------------

#def check_temp_range():
	#global state
   
def temp_control():
	global state
	activation_msg = 1
	
	while (True):
		with config.sensor_lock:
			if (state == 1 and (config.air_temp < config.GOAL_TEMP - config.TEMP_THRESH)):
				if (activation_msg == 1):
					print("Activating heating.")
					activation_msg = 0
				config.board.digital[config.TEMP_CONTROL_PIN].write(1)
			elif (state == 1 and (config.air_temp > config.GOAL_TEMP + config.TEMP_THRESH)):
				if (activation_msg == 1):
					print("Activating cooling.")
					activation_msg = 0
				config.board.digital[config.TEMP_CONTROL_PIN].write(1)
			else:
				if (activation_msg == 0):
					print("Goal Temperature is reached, deactivating cooling.")
					activation_msg = 1

				config.board.digital[config.TEMP_CONTROL_PIN].write(0)
			time.sleep(config.SAMPLE_TEMP_DELAY)
   
def update_temp_state(temp_state):
	global state
	state = 0 if temp_state == 'OFF' else 1
	if (state == 1):
		print("Temperature Controller is ON", flush=True)
	else:
		print("Temperature Controller is OFF", flush=True)
		
	return

def init_temp_system():
	global state
	state = 0
	
	temp_thread = threading.Thread(target=temp_control)
	temp_thread.daemon = True
	temp_thread.start()
