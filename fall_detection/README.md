## Code Organization

This directory contains all folders, python files, and scripts specific to the fall detection module.

### Subdirectories

A brief overview of the contents of each directory/file is explained below. Each directory will have an individual README within that contains more detail.

fall_detection-v3: contains the model of the fall detection classification model trained from Edge Impulse Studio.
subscriber: contains the MQTT files for running subscribers and publishers.
fall_deteect_message.py: the python file for sending the email.
while_loop.sh: the shell script for running the subscriber, fall detection analysis, and emailing.
while_loop_gps.sh: shell script for running updates on the current GPS location.
shell_script_new.sh: overall shell script for running both while loop shell scripts.

### Sources

Fall Detection: https://www.hackster.io/naveenbskumar/fall-detection-system-with-edge-impulse-and-blues-wireless-a4dbba

Emailing: https://mailtrap.io/blog/python-send-email-gmail/

GPS with Notecard: https://dev.blues.io/guides-and-tutorials/notecard-guides/asset-tracking/
