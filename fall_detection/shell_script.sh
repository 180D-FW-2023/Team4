#!/bin/bash
clear
echo "running first test"
while true
{
    ./subscriber/bin/simple_subscriber
    wait
    ./fall_detection-v3/build/app
}
