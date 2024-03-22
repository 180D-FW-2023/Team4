## Code Organization
This directory contains all folders, python files, and examples specific to BerryIMU's accelerometer MQTT process.

### Subdirectories
A brief overview of the contents of each directory/file is explained below.

bin: the binaries after running make.
examples: some of the examples that go into how publishers and subscribers could work. In our case, `simple_subscriber`, `simple_publisher`, and `gps_subscriber` are used here.
gyro_accelerometer_tutorial01_angles: taken from the official BerryIMU GitHub, the files that are required to run the subscriber while reading accelerometer data are put here.
include: some files necessary for MQTT to work.
src: expands on the files in `/include`.
run_publisher.py: file put on the Raspberry Pi to run the publisher on startup. 

### Sources
BerryIMU: https://github.com/ozzmaker/BerryIMU

MQTT in C: https://github.com/LiamBindle/MQTT-C/tree/master
