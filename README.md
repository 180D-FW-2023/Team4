# MemoryMate
The MemoryMate is a device that helps people who struggle with Alzheimer's, some form of dementia, and face blindness, in the elderly community. It has several features: face recognition, step counter, and fall detection. 
Face recognition allows the user to upload photos to add to the database, which will identify anyone the user sees. Step counter counts the number of steps the user has taken to track their health. Fall detection will trigger when the user falls to the ground.

## Fall Detection
Begin by navigating to the fall detection folder with:
`cd fall_detection`

Make the binaries needed for launching the subscriber and publisher by going to the subscriber folder:
```console
cd subscriber
make clean
make bin
make simple_subscriber
make simple_publisher
```

Then launch the subscriber and the fall detection model by running the shell script after going back to the previous folder:
```console
cd ..
sh shell_script.sh
```
You may need to give the file permission with:
`chmod +x shell_script.sh`

Next, ssh into the Raspberry Pi and navigate to the folder for the publisher:
```console
cd subscriber
./bin/simple_publisher
```
