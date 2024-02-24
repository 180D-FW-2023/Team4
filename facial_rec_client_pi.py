from http import client
import io
import socket
import struct
import time
import picamera
import os
import paho.mqtt.client as mqtt
import multiprocessing

def start_client(ip_addr):
    try:
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
        client.sendall("face recognition".encode())
        connection = client.makefile('wb')
        
        p0 = multiprocessing.Process(target=get_images, args=(connection, client))
        p0.start()
        
        p1 = multiprocessing.Process(target=recv_data, args=(client,))
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

def recv_data(client):
    while True:
        name = client.recv(1024).decode()
        print('Received from server: ' + name)  # show in terminal (for now)
        # with open('./nn.txt', 'w') as f:
        #     f.write(str(name))
        os.system('espeak ' + name + ' 2>/dev/null')
	
def get_images(connection, client):
    try:
        camera = picamera.PiCamera()
        camera.resolution = (640, 480)
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        time.sleep(2)

        # Note the start time and construct a stream to hold image data
        # temporarily (we could write it directly to connection but in this
        # case we want to find out the size of each capture first to keep
        # our protocol simple)
        start = time.time()
        stream = io.BytesIO()
        for foo in camera.capture_continuous(stream, 'jpeg'):
            # Write the length of the capture to the stream and flush to
            # ensure it actually gets sent
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            # Rewind the stream and send the image data over the wire
            stream.seek(0)
            connection.write(stream.read())
            # Reset the stream for the next capture
            stream.seek(0)
            stream.truncate()
        # Write a length of zero to the stream to signal we're done
        connection.write(struct.pack('<L', 0))
    finally:
        connection.close()
        client.close()

# def main():
#     if len(sys.argv) != 2:
#         print("Wrong Input")
#         return
#     # TODO: validate a correct ip address

#     # Connect a client socket to server
#     client_socket = socket.socket()
#     client_socket.connect((str(sys.argv[1]), 8080))
#     client_socket.sendall("face recognition".encode())
#     connection = client_socket.makefile('wb')

#     p0 = multiprocessing.Process(target=get_name, args=(client_socket,))
#     p0.start()

#     try:
#         camera = picamera.PiCamera()
#         camera.resolution = (640, 480)
#         # Start a preview and let the camera warm up for 2 seconds
#         camera.start_preview()
#         time.sleep(2)

#         # Note the start time and construct a stream to hold image data
#         # temporarily (we could write it directly to connection but in this
#         # case we want to find out the size of each capture first to keep
#         # our protocol simple)
#         start = time.time()
#         stream = io.BytesIO()
#         for foo in camera.capture_continuous(stream, 'jpeg'):
#             # Write the length of the capture to the stream and flush to
#             # ensure it actually gets sent
#             connection.write(struct.pack('<L', stream.tell()))
#             connection.flush()
#             # Rewind the stream and send the image data over the wire
#             stream.seek(0)
#             connection.write(stream.read())
#             # Reset the stream for the next capture
#             stream.seek(0)
#             stream.truncate()
#         # Write a length of zero to the stream to signal we're done
#         connection.write(struct.pack('<L', 0))
#     finally:
#         connection.close()
#         client_socket.close()

# def get_name(client):
#         #Recieve the name message from the server
#         name = client.recv(1024).decode()
#         print('Received from server: ' + name)  # show in terminal (for now)
#         # with open('./nn.txt', 'w') as f:
#         #     f.write(str(name))
#         os.system('espeak ' + name + ' 2>/dev/null')

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
