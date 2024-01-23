clear
echo "running first test"
while true
do
    ./subscriber/bin/simple_subscriber
    wait
    ./fall_detection-v3/build/app
done
