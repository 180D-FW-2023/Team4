# Code Organization
This directory contains latency measurements for the step count module and a python script to analyze them.

## Files
The purpose of each file will be explained below
- `latency_*.txt`: each of these files has latency measurements that were copied from the command line when the server was runninng and printing time deltas relevant to the measurement in the name of the specific file
- `latency.py`: a python script that analyzes these latency measurements by finding parameters such as the min, max, and average of the dataset as well as plotting the data
