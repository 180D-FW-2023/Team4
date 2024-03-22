from http import client
import io
import socket
import struct
import time
import picamera
import os
import paho.mqtt.client as mqtt
import subprocess
import multiprocessing

def start_client(ip_addr):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(20)
        counter = 0
        while True:
            try:
                client.connect((ip_addr, 8080))
            except:
                counter += 1
                if counter == 5:
                    main()
                    print("starting main again to relook at mqtt")
                    return
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
        print("No camera1")
        if p0.is_alive():
            p0.terminate()
        if p1.is_alive():
            p1.terminate()
        print("starting again")
        p0.join()
        p1.join()
        time.sleep(5)
        main()

def recv_data(client):
    #now = datetime.now()
    try:
        while True:
            name = client.recv(1024).decode()
            os.system('espeak "'+name+'" --stdout | paplay -v')
    except socket.timeout:
        recv_data(client)
	
def get_images(connection, client):
    try:
        try:
            camera = picamera.PiCamera()
        except:
            print("heyyo")
        camera.resolution = (640, 480)
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        time.sleep(2)

        # Note the start time and construct a stream to hold image data
        # temporarily (we could write it directly to connection but in this
        # case we want to find out the size of each capture first to keep
        # our protocol simple)
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
    except:
        print("No camera")
        s = "No camera"
        client.send(s.encode())
    finally:
        connection.close()
        client.close()

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

def main():
    with open('/home/pi/bluetooth.txt', 'r') as f:
        fb = f.read().splitlines()[1]
    subprocess.call(['sudo', 'bluetoothctl', '--', 'disconnect', fb])
    subprocess.call(['sudo', 'bluetoothctl', '--', 'connect', fb])
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
