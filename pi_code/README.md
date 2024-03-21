# Code Organization
This directory contains code that gets put onto the pis through the Initial Setup GUI page. Each of these scripts run on the pi during boot.

## Files
The purpose of each file will be explained below
- `bluetooth.sh`: TODO: krisha
- `facial_rec_client_pi.py`: TODO: krisha/maya
- `step_count_client_pi.py`: a python script that runs on the step counter pi on boot which serves as the client TCP connection to read accelerometer data and send it to the server for processing as well as receive the current step count that it can display
    - Sources:
      - MQTT: Lab 3: Communication from Q1 
      - TCP: https://realpython.com/python-sockets/
      - Multiprocesssing: https://www.digitalocean.com/community/tutorials/python-multiprocessing-example
      - SenseHat: https://projects.raspberrypi.org/en/projects/getting-started-with-the-sense-hat/8
   - Decisions: It was decided to run all this code on the pi on boot which was achieved by editing the rc.local file. Additionally, TCP was chosen as the communication method since it is fully duplex so boht the client and server could both send and receive. This seemed more intuitive than the publisher subscriber method of MQTT.
   - Bugs: If the joystick button on the Pi is pressed to display the step count before the first message of the current step count is received from the server, it falsely displays 0.
   - Future Improvements: Research a polling mechanism to wake the main thread when the server is ready for TCP since the current model continuously gets the retained IP on the MQTT topic and tries to connect which is a waste of power.
