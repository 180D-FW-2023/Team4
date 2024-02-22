from sense_hat import SenseHat
from datetime import datetime
import socket
import sys
import multiprocessing
import time
import os
from signal import SIGKILL

from sense_hat import SenseHat

def main():
	sense = SenseHat()
	
	if len(sys.argv) != 2:
		print("Wrong Input")
		return

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((str(sys.argv[1]), 8080))
	client.sendall("step count".encode())

	p0 = multiprocessing.Process(target=write_acc, args=(sense, client,))
	p0.start()

	p1 = multiprocessing.Process(target=recv_data, args=(sense, client,))
	p1.start()

	while True:
		time.sleep(1)
		if not p0.is_alive():
			p1.terminate()
			p0.join()
			p1.join()
			break
		elif not p1.is_alive():
			p0.terminate()
			p1.join()
			p0.join()

def recv_data(sense, client):
	def print_num(event):
		if event.action == 'pressed':
			sense.show_message(str(step_count))
	
	step_count = 0
	sense.stick.direction_any = print_num

	while True:
		recv_data = client.recv(4096).decode('utf_8')
		num = recv_data.split(";")
		if(len(num) >= 2):
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