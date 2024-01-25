from sense_hat import SenseHat
from datetime import datetime
import socket
import sys
import multiprocessing

from sense_hat import SenseHat

def main():
	def print_num(event):
		if event.action == 'pressed':
			sense.show_message(str(step_count))

	sense = SenseHat()
	step_count = 0
	sense.stick.direction_any = print_num
    # TODO: error handling
	if len(sys.argv) != 2:
		print("Wrong Input")
		return
	# TODO: validate a correct ip address

	# TODO: check all return values
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((str(sys.argv[1]), 8080))
	client.sendall("step count".encode())

	p0 = multiprocessing.Process(target=write_acc, args=(sense, client,))
	p0.start()

	sense.show_message("hi")
	while True:
		recv_data = client.recv(4096).decode('utf_8')
		num = recv_data.split(";")
		assert(len(num) >= 2)
		step_count = num.pop(-2)

def write_acc(sense, client):
	count = 0
	while True:
		count = count + 1
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