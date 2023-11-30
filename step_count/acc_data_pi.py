from sense_hat import SenseHat
from datetime import datetime
import socket

sense = SenseHat()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('169.232.86.224', 8080))

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

	line = date + "," + time + "," + acc + ";"
	print(line)
	client.sendall(line.encode())