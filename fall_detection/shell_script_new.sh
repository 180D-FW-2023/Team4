clear
echo "running first test"
while true
do
    /Users/Home/Team4/fall_detection/subscriber/bin/simple_subscriber
    wait
    /Users/Home/Team4/fall_detection/fall_detection-v3/build/app
done
