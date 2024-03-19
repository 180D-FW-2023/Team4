# MemoryMate
The MemoryMate is a device that helps people who struggle with Alzheimer's, some form of dementia, and face blindness, in the elderly community. It has several features: face recognition, step counter, and fall detection. 
Face recognition allows the user to upload photos to add to the database, which will identify anyone the user sees. Step counter counts the number of steps the user has taken to track their health. Fall detection will trigger when the user falls to the ground, then email close contacts with the user's current location.

## Code Organization
The main repository is split into all of its major components, including product functions, GUI, and interactions with Raspberry Pi.
`face_recog`, `fall_detection`, and `step_count` contain the code for the 3 modules of the device.
- `face_recog`:
- `fall_detection`: uses MQTT to receive GPS data from the Blues Wireless Notecard and accelerometer data from the BerryIMU.
- `step_count`:

`gui`, `gui_txt_files`, and `pages` consist of code that makes up the display and user interface.
- `gui`:
- `gui_txt_files`:
- `pages`:

## Cloning and Installing Dependencies
Begin by cloning this repository and navigating to the Team4 folder. Run the following commands to make the binaries for fall detection:
```
cd fall_detection/fall_detection-v3
make clean
make -j4
cd ../subscriber
make clean
make bin
make bin/simple_subscriber
make bin/gps_subscriber
cd ../..
```

Now, we will install the remaining dependencies in a virtual environment by running the following commands:
```
cd gui
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
brew install esolitos/ipa/sshpass
deactivate
```

Finally, make sure you have executable permissions by running the following commands:
```
chmod +x ../fall_detection/while_loop_gps.sh
chmod +x ../fall_detection/while_loop.sh
```

## Start Up the GUI and Setup
Start up your virtual environment again and run the GUI:
```
source venv/bin/activate
streamlit run Welcome.py
```

The GUI should pop up in a new page on your browser. First, navigate to the Load Facial Recognition Data page. 
Add 5-10 pictures for each person to be identified with the correct name. Make sure you click "Upload files" for each person! After all your photos are uploaded, go ahead and click the retrain button to update the facial recognition model.
<img width="1293" alt="Screenshot 2024-02-20 at 1 01 28 PM" src="https://github.com/180D-FW-2023/Team4/assets/29986734/dfb77f19-de3c-4be0-8354-965ddd031137">

## Run the Server:
With the GUI still running, navigate to the Run Server page and click the button to run it. After you hit the button, it may take a few minutes to get booted up and start working. While the server is running, you can navigate to the Fall Detection, Recognized Face, and Step Count pages to view subsystem specific output. To get a cohesive view of the output, you can also navigate to the Overall Output page. Once you are finished running the server, navigate back to the Run Server page and click the Stop server button.

## Stopping the GUI
Once you are finished, you can stop the GUI and exit the virtual environment by running the following commands from the terminal where you started the GUI.
```
Ctrl-C
deactivate
```
## Setting Up The Physical Product
### Fall Detection
![20240306_180011](https://github.com/180D-FW-2023/Team4/assets/85961054/8c850235-876d-40bd-95c5-7a142be475dd | width=100)
Connect the powerbank to the power ports on the Notecard and the Raspberry Pi (with 2 USB-A to micro USB cables). The lights on the powerbank should turn on. Once the lights are on, hold the power button on the side of the power bank until the lights start flashing in order. 

![image](https://github.com/180D-FW-2023/Team4/assets/85961054/2d186a97-198b-4c7f-9d57-c9590cd87366)
![image](https://github.com/180D-FW-2023/Team4/assets/85961054/0d06beb7-a26d-4c09-a8b6-02bc3275b30f)
Place the powerbank and Notecard/Notecarrier into the pouch, then place the Raspberry Pi into one of the outside pockets with the Micro-USB connection pointing up.
Place the pouch into the center pocket of the sweatshirt, zipper on the top side.

### Face Recognition
![IMG_20240220_140318](https://github.com/180D-FW-2023/Team4/assets/33609544/10571175-d382-419c-b4a3-787b5cf39251)
Connect the camera to the Raspberry Pi and connect the power bank/battery to the Pi. Velcro the Pi and battery into the shoulder pouch inside the sweatshirt, and put the camera through the slit
![20240310_171827 (1)](https://github.com/180D-FW-2023/Team4/assets/85961054/54a0b7fe-bc42-446f-8c95-8c07f6085316)

### Step Counter

Power on the battery for the Raspberry Pi by pressing the button circled in red below once. To turn it off, press the button twice. The pi has finished booting once the rainbow display on the LED display turns off.

<img width="371" alt="image" src="https://github.com/180D-FW-2023/Team4/assets/103907560/009759c6-c70b-412e-ac86-f3be8ebe9c9f">

Place it in the wrist pocket such that the LED display is facing outwards. The button circled in red in the image below indicates the bottom right of the device (for display purposes). You can orient the device however you may like within the pocket.

![20240310_171713](https://github.com/180D-FW-2023/Team4/assets/85961054/afcf6a3d-da1d-4492-8a85-f07ddb56356e)
<img width="308" alt="image" src="https://github.com/180D-FW-2023/Team4/assets/103907560/c2d69d28-59fc-4381-995c-ee198fc6331a">

When the server is running, you can press the button circled in red in the image above to see your current daily step count show on the LED display.




