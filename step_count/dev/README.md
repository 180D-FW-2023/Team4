# Code Organization
This directory contains python scripts that can run different step count algorithms on .csv files

## Files
The purpose of each file will be explained below.
- `smooth_step_count.py`: a python script that finds the number of steps taken based on accelerometer data smoothed with the Savitzky-Golay filter
    - Sources:
        - https://dwightreid.com/site/how-to-count-steps-using-python-data-analysis-of-acceleration-data/
        - https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_filter.html
- `step_count.py`: a python script that finds the number of steps taken based on raw accelerometer data
    - Source: https://dwightreid.com/site/how-to-count-steps-using-python-data-analysis-of-acceleration-data/
