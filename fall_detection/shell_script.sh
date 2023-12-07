#!/bin/bash
clear
echo "running first test"
./subscriber/bin/simple_subscriber
wait
./fall_detection-v3/build/app
exit 0
