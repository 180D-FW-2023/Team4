from http import client
import io
import socket
import struct
import time
import picamera
import os
import sys
import multiprocessing

def main():
    if len(sys.argv) != 2:
        print("Wrong Input")
        return
    # TODO: validate a correct ip address

    print("here2")

    # Connect a client socket to my_server:8000 (change my_server to the
    # hostname of your server)
    client_socket = socket.socket()
    client_socket.connect((str(sys.argv[1]), 8080))
    client_socket.sendall("face recognition".encode())
    connection = client_socket.makefile('wb')

    p0 = multiprocessing.Process(target=get_name, args=(client_socket,))
    p0.start()

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
            # If we've been capturing for more than 30 seconds, quit
            if time.time() - start > 60:
                break
            # Reset the stream for the next capture
            stream.seek(0)
            stream.truncate()
        # Write a length of zero to the stream to signal we're done
        connection.write(struct.pack('<L', 0))
    finally:
        connection.close()
        client_socket.close()

def get_name(client):
        #Recieve the name message from the server
        name = client.recv(1024).decode()
        #print('Received from server: ' + name)  # show in terminal (for now)
        with open('./nn.txt', 'w') as f:
            f.write(str(name))
        #os.system('espeak ' + name + ' 2>/dev/null')

if __name__ == "__main__":
    main()