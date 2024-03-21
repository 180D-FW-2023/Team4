# Code Organization
This directory contains all accelerometer and step count data that the raspberry pi takes and sends to the server over the TCP connection

## Files
The purpose of each file will be explained below.
- `YEAR-MONTH-DAY_HOUR.csv`: accelerometer data for the given hour in the name of the file written to by `server.py`
- `YEAR-MONTH-DAY_total.csv`: step count totals overall and per hour for the given day written to by `server.py`
