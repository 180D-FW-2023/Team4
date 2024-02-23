from sense_hat import SenseHat
from datetime import datetime
import socket
import multiprocessing
import time
from signal import SIGKILL
import paho.mqtt.client as mqtt
from sense_hat import SenseHat

def start_client(ip_addr):
	try:
		sense = SenseHat()

		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		while True:
			try:
				client.connect((ip_addr, 8080))
			except:
				time.sleep(2)
				print("failed at socket connection")
				continue
			else:
				break
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
	# if any errors or processes terminate, run main again
	finally:
		time.sleep(2)
		main()

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

# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/ece180d/team4/setup", qos=1)

# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

# The default message callback.
# (you can create separate callbacks per subscribed topic)
def on_message(client, userdata, message):
    msg_recv = str((message.payload).decode('utf_8').strip('\n'))
    print('Received message: "' + msg_recv + '" on topic "' + message.topic + '" with QoS ' + str(message.qos))
    client.loop_stop()
    client.disconnect()
    start_client(msg_recv)

def mqtt_create_sub():
	# 1. create a client instance.
	client = mqtt.Client()
	# add additional client options (security, certifications, etc.)
	# many default options should be good to start off.
	# add callbacks to client.
	client.on_connect = on_connect
	client.on_disconnect = on_disconnect
	client.on_message = on_message

	# 2. connect to a broker using one of the connect*() functions.
	client.connect_async('test.mosquitto.org')
	# client.connect("mqtt.eclipse.org")

	# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
	# client.loop_start()
	client.loop_forever()
	print("here")

def main():
	while True:
		try:
			mqtt_create_sub()
		except:
			time.sleep(2)
			print("failed at starting mqtt")
			continue
		else:
			break

if __name__ == "__main__":
	main()
