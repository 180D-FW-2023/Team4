# MemoryMate
The MemoryMate is a device that helps people who struggle with Alzheimer's, some form of dementia, and face blindness, in the elderly community. It has several features: face recognition, step counter, and fall detection. 
Face recognition allows the user to upload photos to add to the database, which will identify anyone the user sees. Step counter counts the number of steps the user has taken to track their health. Fall detection will trigger when the user falls to the ground.

## Fall Detection
Begin by navigating to the fall detection folder with:
`cd fall_detection`

Make the binaries needed for launching the subscriber and publisher by going to the subscriber folder:
```shell
cd subscriber
make clean
make bin
make simple_subscriber
make simple_publisher
```

Then launch the subscriber and the fall detection model by running the shell script after going back to the previous folder:
```shell
cd ..
sh shell_script.sh
```
You may need to give the file permission with:
`chmod +x shell_script.sh`

Next, ssh into the Raspberry Pi and navigate to the folder for the publisher:
```shell
cd subscriber
./bin/simple_publisher
```
## Facial Recognition and Step Count

### Setup:
2. Get the ip address of your laptop that will be acting as the server: `ipconfig getifaddr en0`
3. In the client code stream_client.py, replace '192.168.1.104' in `client_socket.connect(('192.168.1.104', 8000))` and in step_count_client_pi.py, replace '192.168.1.199' in `client.connect(('192.168.1.199', 8080))` with your laptop's ip address
4. ssh into your two Raspberry Pis. One pi (pi 1) will be for facial recognition and the other (pi 2) will be for the step counter
5. Copy stream_client.py onto pi 1 and step_count_client_pi.py onto pi 2 (that have your changes from step 2)
6. On your server you will need to install the packages used in server.py: `pip install socket matplotlib.pyplot numpy scipy.signal multiprocessing io struct PIL cv2 face_recognition argparse pathlib collections pickle`
7. On pi 1 you will need to install the packages used in TBD: `pip install socket io picamera struct time`
8. On pi 2 you will need ot install the packages used in step_count_client_pi.py `pip install sense_hat datetime socket`

## Run the Code
Now that you have finished setup, you can now run everything!
1. Start up the server code (server.py) on your laptop: `python3 server.py`
2. Run the client code on your two pis in any order
   1. pi 1 with TBD: `python stream_client.py`
   2. pi 2 with step_count_client_pi.py: `python3 step_count_client_pi.py`
