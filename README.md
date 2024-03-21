# MemoryMate
The MemoryMate is a device that helps people who struggle with Alzheimer's, some form of dementia, and face blindness, in the elderly community. It has several features: face recognition, step counter, and fall detection. 
Face recognition allows the user to upload photos to add to the database, which will identify anyone the user sees. Step counter counts the number of steps the user has taken to track their health. Fall detection will trigger when the user falls to the ground.

## Code Organization
The main repository is split into all of its major components, including product functions, GUI, and interactions with Raspberry Pi. 

### Subdirectories
A brief overview of the contents of each directory is explained below. Each directory will have an individual README within that contains more detail. 
- `face_recog`: TODO: krisha/mayaa
- `fall_detection`: uses MQTT to receive GPS data from the Blues Wireless Notecard and accelerometer data from the BerryIMU
- `gui_txt_files`: contains all files the server code writes to that the GUI reads to update each page
- `pages`: TODO: krisha
- `pi_code`: contains code that gets put onto the pis through the Initial Setup GUI page
- `step_count`: contains data that the step count module collects whie running, latency measurements, and some developental code for step counter algorithms

### Files
The purpose of each file will be explained below
- `__init__.py`: 
   - Sources: TODO: krisha
- `server.py`: 
   - Sources:
      - MQTT: Lab 3: Communication from Q1 
      - TCP: https://realpython.com/python-sockets/
      - Multiprocesssing: https://www.digitalocean.com/community/tutorials/python-multiprocessing-example
      - Step Count Algorithm (`step_count()`): https://dwightreid.com/site/how-to-count-steps-using-python-data-analysis-of-acceleration-data/, https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_filter.html
      - read .csv data: https://stackoverflow.com/questions/68359017/numpy-genfromtxt-skip-invalid-lines
      - TODO: image stuff
   - Decisions: We decided to run every process with a new Multiprocessing Processs to keep them self-contained and isolated. Additionally, it was decided to implement the facial recognition and step count modules with TCP for communication, whereas the fall detection module uses MQTT.
   - Bugs: None that we know of and all should be handled by the try except blocks.
   - Future Improvements: Improve on process clean up by potentially switching to a Multiprocessing Pool so that on a control-C, every process terminates nicely. Currrently this is handled manually in the GUI Run Server page by manually killing all processes spawned.
- `requirements.txt`: TODO: krisha
- `user_manual.md`: the user manual for how to setup and run the system utilizing the code in this repo
- `Welcome.py`: TODO: krisha
