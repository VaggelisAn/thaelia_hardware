Code for the Hardware of team Thaelia (iGEM Thessaly 2024).
Our project aims to develop a bacterial formulation to protect olive trees from Verticillium dahliae. 
The treatment involves using engineered P. putida to facilitate bacterial-mediated RNA interference (bmRNAi).
To ensure the safety and efficacy of our bacterial system, we developed tools to monitor and test its behaviour under controlled conditions. 
This collaborative effort addresses a fundamental question in biosafety: "How safe is safe?"
For more information on our project, visit our wiki: https://2024.igem.wiki/thessaly/
For more information on our hardware, visit our hardware page https://2024.igem.wiki/thessaly/hardware
To see more projects from the iGEM Thessaly team, visit: https://igem-thessaly.uth.gr/

The code is also hosted on our team's GitLab: 

Our code is split into several python files, each containing a number of modules.
However, we can separate the code in the following categories:
UI: HTML, CSS and Javascript comprise the Hardware’s Frontend. These webpages are hosted on a local server (default address is: localhost:8080/).
Sensors: Air Temperature, Air Humidity, Pot Moisture and of course, VOC concentration measuring and plotting. The measurements are stored inside globally declared variables, so they may be used inside their respective control functions.
Control functions: Temperature, irrigation frequency and amount, and VOC sampling are controlled inside these files through the Arduino.
Arduino: The Arduino runs the StandardFirmata.ino code provided with the Arduino IDE. This script allows a computer (connected to the Arduino through a USB) to control each pin. All control functions described above basically control Arduino digital pins.
Thread Initialization is done through the main.py file.

Regarding threads:
The main thread runs the UI on the local server (through the bottle library).
Each control function belongs to a separate thread, so that they all may run in parallel.
Sensor sampling is also done on one thread, while plotting (through matplotlib) is done on a separate thread.
