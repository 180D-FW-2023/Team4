from sense_hat import SenseHat
from datetime import datetime
import sys
import numpy as np
from scipy.signal import find_peaks
from scipy.signal import savgol_filter

path = "./data/"

def main():
	sense = SenseHat()
	# TODO: error handling
	if len(sys.argv) != 2:
		print("Wrong Input")
		return
	# TODO: validate a correct ip address
	
	current_date = ""
	current_hour = ""
	day_step_count = 0
	
	hour_data = 0
	file_name = None
	file = None

	while True:
		# accelerometer data
		acceleration = sense.get_accelerometer_raw()
		x = acceleration['x']
		y = acceleration['y']
		z = acceleration['z']

		acc = str(x) + "," + str(y) + "," + str(z)

		# data and time
		now = datetime.now()
		date = now.strftime("%Y-%m-%d")
		time = now.strftime("%H:%M:%S.%f")

		line = date + "," + time + "," + acc
		print(line)
		list_item = line.split(",")
		if len(list_item) != 5:
			continue
		if len(list_item[0]) != 10:
			continue
		# TODO: thread/process parallelize this
		# TODO: make it user input?
		hour_data += 1
		if file_name and hour_data % 50 == 0:
			file.close()
			cur_step_count = day_step_count + step_count(file_name)
			file = open(file_name,"a")
			print("Step Count: " + str(cur_step_count))
		# in current date and hour
		if list_item[0] == current_date and list_item[1][0:2] == current_hour:
			if file:
				file.write(line + "\n")
		# in current date, new hour
		elif list_item[0] == current_date and list_item[1][0:2] != current_hour:
			if file:
				file.close()
				# TODO: make this a new process so parallelism
				day_step_count += step_count(file_name)
			print("Current Step Count: " + str(day_step_count))
			current_hour = list_item[1][0:2]
			file_name = path + current_date + "_" + current_hour + ".csv"
			file = open(file_name,"a")
			file.write(line + "\n")
		# in new date
		else:
			if file:
				file.close()
			# TODO: store step count data
			day_step_count = 0
			current_date = list_item[0]
			current_hour = list_item[1][0:2]
			file_name = path + current_date + "_" + current_hour + ".csv"
			file = open(file_name,"a")
			file.write(line + "\n")

def convert_strings_to_floats(input_array):
    output_array = []
    for element in input_array:
        converted_float = float(element)
        output_array.append(converted_float)
    return output_array

def step_count(path_name):
    data = np.loadtxt(path_name, delimiter =',', dtype = str)

    xdata = convert_strings_to_floats(data[:,2])
    ydata = convert_strings_to_floats(data[:,3])
    zdata = convert_strings_to_floats(data[:,4])

    accel_mag = np.sqrt((np.power(xdata, 2) + np.power(ydata, 2) + np.power(zdata, 2)))
    accel_mag = accel_mag - np.mean(accel_mag)
    
    y_smooth = savgol_filter(accel_mag, window_length=40, polyorder=3, mode="nearest")
    smooth_peaks, _ = find_peaks(y_smooth, height=0.2)

    total_peaks = len(smooth_peaks)

    return total_peaks

if __name__ == "__main__":
    main()