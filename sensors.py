import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import board
import adafruit_shtc3
import threading
import config
import RPi.GPIO as GPIO
import warnings
import busio
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

#global i2c, spi, cd, mcp
def read_shtc3():
    global sht
    try:
        temperature, humidity = sht.measurements

		# sensor_lock syncs temp control thread + temp sensor thread
        #with config.sensor_lock:
        config.air_temp = temperature 
        config.air_humidity = humidity
        
        config.temp_file.write(f"{temperature}\n")
        config.air_hum_file.write(f"{humidity}\n")

        #print("Temperature: %0.1f C" % temperature)
        #print("Humidity: %0.1f %%" % humidity)
    except Exception as error:
        print(f"Error: {error}")
        temperature, humidity = (-1, -1)
    return (temperature, humidity)

def read_hygrometers():
    GPIO.setmode(GPIO.BCM)
    count_high_pins = 0
    high_pins_to_activation = 3
    
    # Sample 8 hygrometers:
    for hygr_pin in range(config.HYGR_PIN_OFFSET, config.HYGR_PIN_OFFSET+config.NUM_OF_HYGR_SENSORS):
        GPIO.setup(hygr_pin, GPIO.IN)
        if (GPIO.input(hygr_pin) == GPIO.HIGH):
            print(f"Plant connected to pin#{hygr_pin} requires watering")
            count_high_pins += 1
    
    if (count_high_pins > high_pins_to_activation):
        print(f"More than {high_pins_to_activation} plants require watering, enabling irrigation")
        return 1
        
    return 0

# For MQ-3 Alchohol Sensor:
def read_voc_sensor():
    global channel_0
    try:
        #print(f"channel 0 (mq3) = {channel_0.value}")
        return channel_0.value
    except:
        return -1

# This function is called periodically from FuncAnimation
def animate(frame):
    global time_counter
    global fig, ax1, ax2, ax3, xs, ys_temp, ys_humidity, ys_vocs, line1, line2, line3

    # Read temperature (Celsius) from shtc3
    temp, humidity = read_shtc3()
    
    # VOC (MQ-3) readings:
    vocs = read_voc_sensor()
    config.voc_file.write(f"{vocs}\n")

    # Add x and y to lists
    xs.append(time_counter)
    time_counter += 1
        
    # If shtc3 sensor returns error repeat previous values
    if (humidity == -1 and len(ys_humidity)>0):
        ys_temp.append(ys_temp[-1])
        ys_humidity.append(ys_humidity[-1])
    else:
        ys_temp.append(temp)
        ys_humidity.append(humidity)
    
    # If VOC sensor return error (-1) repeat previous values
    if (vocs == -1 and len(ys_vocs)>0):
        ys_vocs.append(ys_vocs[-1])
    else:
        ys_vocs.append(vocs)
    

    line1.set_data(xs, ys_temp)
    line2.set_data(xs, ys_humidity)
    line3.set_data(xs, ys_vocs)
    
    if time_counter >= ax1.get_xlim()[1]:
        ax1.set_xlim(ax1.get_xlim()[0], time_counter + 60)
        ax2.set_xlim(ax2.get_xlim()[0], time_counter + 60)
        ax3.set_xlim(ax3.get_xlim()[0], time_counter + 60)

    return line1, line2, line3

def init_plot():
    global fig, ax1, ax2, ax3, xs, ys_temp, ys_humidity, ys_vocs, line1, line2, line3
    global time_counter
    
    # Create figure for plotting
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 8))
    xs = []
    ys_temp = []
    ys_humidity = []
    ys_vocs = []

    time_counter = 0

    line1, = ax1.plot([], [], lw=2, label='Air Temperature')
    line2, = ax2.plot([], [], lw=2, label='Air Humidity')
    line3, = ax3.plot([], [], lw=2, label='VOCs')

    ax1.set_xlim(0, 20)
    ax1.set_ylim(10, 40)

    ax2.set_xlim(0, 20)
    ax2.set_ylim(0, 100)
    
    ax3.set_xlim(0, 20)
    ax3.set_ylim(10000, 70000)

    ax1.set_title("Air Temperature")
    ax2.set_title("Air Humidity")
    ax3.set_title("VOCs")
    ax1.set_ylabel("Air Temperature (C)")
    ax2.set_ylabel("Air Humidity (%RH)")
    ax3.set_ylabel("VOCs")
    ax1.set_xlabel("Time (s)")
    ax2.set_xlabel("Time (s)")
    ax3.set_xlabel("Time (s)")

def sensors_system():
    global sht, channel_0
    MAX_FRAMES = 10000
    
    # - - BOARD - -
    i2c = board.I2C()   # uses board.SCL and board.SDA
    # Create the SPI bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # Create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # Create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    # - - SENSORS - -    
    sht = adafruit_shtc3.SHTC3(i2c)
    channel_0 = AnalogIn(mcp, MCP.P0) # MQ-3/ VOC Sensor Pin -> MC3008
    voc_values_file = open("voc_values.txt", "a")

        # - - PLOTS - -
    init_plot()
    ani = animation.FuncAnimation(fig, animate, interval=1000, save_count=MAX_FRAMES)
    plt.show()

def init_sensors():
    sensor_thread = threading.Thread(target=sensors_system)
    sensor_thread.daemon = True
    sensor_thread.start()
