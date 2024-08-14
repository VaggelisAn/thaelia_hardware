import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import board
import adafruit_shtc3
import threading
import config

def read_shtc3():
    global sht
    try:
        temperature, humidity = sht.measurements

        with config.sensor_lock:
            config.air_temp = temperature
            config.air_humidity = humidity
            print(f"t = {config.air_temp}")
        
        #print("Temperature: %0.1f C" % temperature)
        #print("Humidity: %0.1f %%" % humidity)
    except Exception as error:
        print(f"Error: {error}")
        temperature, humidity = (-1, -1)
    return (temperature, humidity)

# This function is called periodically from FuncAnimation
def animate(frame):
    global time_counter
    global fig, ax1, ax2, xs, ys_temp, ys_humidity, line1, line2

    # Read temperature (Celsius) from TMP102
    temp, humidity = read_shtc3()

    # Add x and y to lists
    xs.append(time_counter)
    time_counter += 1
        
    # If sensor returns error repeat previous values
    if (humidity == -1 and len(ys_humidity)>0):
        ys_temp.append(ys_temp[-1])
        ys_humidity.append(ys_humidity[-1])
    else:
        ys_temp.append(temp)
        ys_humidity.append(humidity)

    line1.set_data(xs, ys_temp)
    line2.set_data(xs, ys_humidity)
    
    if time_counter >= ax1.get_xlim()[1]:
        ax1.set_xlim(ax1.get_xlim()[0], time_counter + 60)
        ax2.set_xlim(ax2.get_xlim()[0], time_counter + 60)
    
    return line1, line2
    
    # Draw x and y lists
    ax.clear()
    plt.subplot(1, 1, 1)
    ax.plot(xs, ys_temp)
    plt.subplot(2, 1, 1)
    ax.plot(xs, ys_humidity)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Temperature and Humidity over Time')
    plt.ylabel('Temperature (deg C)')

def init_plot():
    global fig, ax1, ax2, xs, ys_temp, ys_humidity, line1, line2
    global time_counter
    # Create figure for plotting
    fig, (ax1, ax2) = plt.subplots(2, 1)
    xs = []
    ys_temp = []
    ys_humidity = []

    time_counter = 0

    line1, = ax1.plot([], [], lw=2, label='Air Temperature')
    line2, = ax2.plot([], [], lw=2, label='Air Humidity')

    ax1.set_xlim(0, 600)
    ax1.set_ylim(10, 40)

    ax2.set_xlim(0, 600)
    ax2.set_ylim(0, 100)

    ax1.set_title("Air Temperature")
    ax2.set_title("Air Humidity")
    ax1.set_ylabel("Air Temperature (C)")
    ax2.set_ylabel("Air Humidity (%RH)")
    ax1.set_xlabel("Time (s)")
    ax2.set_xlabel("Time (s)")
    
def sensors_system():
    global ic2, sht
    MAX_FRAMES = 10000
    
    # - - BOARD - -
    i2c = board.I2C()   # uses board.SCL and board.SDA
        
    # - - SENSORS - -    
    sht = adafruit_shtc3.SHTC3(i2c)
        # - - PLOTS - -
    init_plot()
    ani = animation.FuncAnimation(fig, animate, interval=1000, save_count=MAX_FRAMES)
    plt.show()

def init_sensors():
    sensor_thread = threading.Thread(target=sensors_system)
    sensor_thread.daemon = True
    sensor_thread.start()
