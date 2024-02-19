while true
do
    ./fall_detection/subscriber/bin/simple_subscriber
    wait
    ./fall_detection/fall_detection-v3/build/app
    wait
    python3 fall_detection/fall_detected_message.py
done
