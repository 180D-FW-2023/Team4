from sense_hat import SenseHat
from datetime import datetime
import socket
import sys

def main():
	sense = SenseHat()
	# TODO: error handling
	if len(sys.argv) != 2:
		print("Wrong Input")
		return
	# TODO: validate a correct ip address

	# TODO: check all return values
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((str(sys.argv[1]), 8080))
	client.sendall("step count".encode())

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
		# print(line)
		client.sendall(line.encode())

if __name__ == "__main__":
    main()