#!/bin/bash

sudo bluetoothctl scan on &
sleep 30
sudo bluetoothctl trust $1
sudo bluetoothctl pair $1
sudo bluetoothctl scan off
sudo bluetoothctl connect $1
sudo bluetoothctl connect $1
sudo pkill -f bluetoothctl
