#!/bin/bash
clear
echo "running first test"
while sleep 10
{
    ./subscriber/bin/simple_subscriber
    wait
    ./fall_detection-v3/build/app
}
