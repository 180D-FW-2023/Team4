from sense_hat import SenseHat
from datetime import datetime

sense = SenseHat()

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