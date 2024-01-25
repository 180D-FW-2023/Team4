import socket
#import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import multiprocessing 
import subprocess
import os
from pathlib import Path

import io
import struct
#from PIL import Image
import cv2 as cv
import numpy as np
from face_recog.detector import recognize_faces


# TODO: can this be here?
cwd = os.getcwd()
cwd = cwd[:cwd.find('Team4') + 5]

path = cwd + "/step_count/data/"
step_count_pi_path = "./step_count_client_pi.py"
facial_rec_pi_path = "./facial_rec_client_pi.py"

names = []
total_seen = set()

def main1():
    # TODO: check return values of all following
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Assigns a port for the server that listens to clients connecting to this port.
    serv.bind(('0.0.0.0', 8080))
    serv.listen(5)

    # TODO: only on mac?
    serv_ip_addr = subprocess.run(['ipconfig', 'getifaddr', 'en0'], stdout=subprocess.PIPE)
    serv_ip_addr = serv_ip_addr.stdout.decode()
    print("server ip adddress: " + serv_ip_addr)

    # p3 = multiprocessing.Process(target=server_fall)
    # p3.start()

    # gets step counter pi info
    step_count_info_list = None
    with open("step_count_pi_ip.txt") as file_step_count:
        step_count_info_list = file_step_count.read().splitlines() 
    if(len(step_count_info_list) != 3):
        print("Error: Set Up Your Step Counter Pi")
        return
    
    # step count start pi client code
    p0 = multiprocessing.Process(target=run_pi, args=(step_count_info_list, serv_ip_addr, "step_count" ))
    p0.start()
    print("here 2")

    # facial rec start pi client code
    facial_rec_info_list = None
    with open("facial_rec_pi_ip.txt") as file_facial_rec:
        facial_rec_info_list = file_facial_rec.read().splitlines() 
    # TODO: error handling
    assert(len(facial_rec_info_list) == 3)
    p01 = multiprocessing.Process(target=run_pi, args=(facial_rec_info_list, serv_ip_addr, "facial_rec" ))
    p01.start()
    print("here 3")
    while True:
        print("here")
        conn, addr = serv.accept()
        print(addr)
        first_message = conn.recv(4096).decode('utf_8')
        if (first_message == "step count"):
            p1 = multiprocessing.Process(target=server_step_count, args=(conn, ))
            p1.start()
            # server_step_count(conn)
        if (first_message == "face recognition"):
            p2 = multiprocessing.Process(target=server_face_rec, args=(conn, ))
            p2.start()
        
def convert_strings_to_floats(input_array):
    output_array = []
    for element in input_array:
        converted_float = float(element)
        output_array.append(converted_float)
    return output_array

def step_count(path_name):
    # TODO: error handle?
    data = np.loadtxt(path_name, delimiter =',', dtype = str)

    xdata = convert_strings_to_floats(data[:,2])
    ydata = convert_strings_to_floats(data[:,3])
    zdata = convert_strings_to_floats(data[:,4])

    accel_mag = np.sqrt((np.power(xdata, 2) + np.power(ydata, 2) + np.power(zdata, 2)))
    accel_mag = accel_mag - np.mean(accel_mag)

    # accel_mag = accel_mag - np.mean(accel_mag)
    # min_peak_height = 2*np.std(accel_mag) + np.mean(accel_mag)
    # TODO: tune height, make greater of 1.3 and std dev?
    std_dev_height = np.std(accel_mag)
    height = 0.3
    min_peak_height = std_dev_height if std_dev_height > height else height
    peaks, _ = find_peaks(accel_mag, height=min_peak_height)

    neg_accel_mag = -accel_mag
    neg_std_dev_height = np.std(neg_accel_mag)
    neg_height = 0.18
    neg_min_peak_height = neg_std_dev_height if neg_std_dev_height > neg_height else height
    neg_peaks, _ = find_peaks(neg_accel_mag, height=neg_min_peak_height)

    total_peaks = len(peaks) if len(peaks) < len(neg_peaks) else len(neg_peaks)

    return total_peaks

def server_step_count(conn):
    from_client = ''
    current_date = ""
    current_hour = ""
    day_step_count = 0

    hour_data = 0
    file_name = None
    file = None
    
    while True:
        data = conn.recv(4096)
        if not data: break
        from_client += data.decode('utf_8')
        list_data = data.decode('utf_8').replace("\n", "").split(";")

        for item in list_data: 
            list_item = item.split(",")
            if len(list_item) != 5:
                continue
            if len(list_item[0]) != 10:
                continue
            # TODO: thread/process parallelize this
            hour_data += 1
            if file_name and file and hour_data % 50 == 0:
                file.close()
                cur_step_count = day_step_count + step_count(file_name)
                file = file_open(file_name)
                print("Step Count: " + str(cur_step_count))
            # in current date and hour
            if list_item[0] == current_date and list_item[1][0:2] == current_hour:
                if file:
                    file.write(item + "\n")
            # in current date, new hour
            elif list_item[0] == current_date and list_item[1][0:2] != current_hour:
                if file:
                    file.close()
                    # TODO: make this a new process so parallelism
                    day_step_count += step_count(file_name)
                print("Current Step Count: " + str(day_step_count))
                current_hour = list_item[1][0:2]
                file_name = path + current_date + "_" + current_hour + ".csv"
                file = file_open(file_name)
                file.write(item + "\n")
            # in new date
            else:
                if file:
                    file.close()
                # TODO: store step count data
                day_step_count = 0
                current_date = list_item[0]
                current_hour = list_item[1][0:2]
                file_name = path + current_date + "_" + current_hour + ".csv"
                file = file_open(file_name)
                file.write(item + "\n")
    conn.close()
    print('Step Count Client Disconnected')

def file_open(file_name):
    try: 
        file = open(file_name,"a")
        return file
    except:
        dir = file_name[:file_name.rfind("/")]
        Path(dir).mkdir(parents=True, exist_ok=True)
        return file_open(file_name)

def server_fall():
    subprocess.call(['sh', cwd + '/fall_detection/shell_script.sh'])

def server_face_rec(conn):
    connection = conn.makefile('rb')
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
            #return
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))

        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = cv.imdecode(np.frombuffer(image_stream.read(), np.uint8), cv.IMREAD_COLOR)

            #Save the image to a folder called stream-pics (each image will have a different name)
            # image.save('stream-pics/im' + str(i) + '.png')
        cv.imwrite(cwd + '/face_recog/test.png', image)
        # image = Image.open(image_stream)
        # print('Image is %dx%d' % image.size)
        # image.verify()
        # print('Image is verified')

        names_recognized = recognize_faces(cwd + '/face_recog/test.png')
        for name in names_recognized:
            if name not in total_seen:
                total_seen.add(name)
        if len(total_seen) != 0:
            with open(cwd + '/total_seen.txt', 'w') as f:
                f.write(str(total_seen))
        #print("I passed")

def run_pi(info, server_ip_addr, pi_type):
    pi_ip = info[0]
    pi_user = info[1]
    pi_pswd = info[2]
    # TODO: is this right for resiliency?
    while True:
        if pi_type == "step_count":
            # TODO: what if bad password/host/ip?
            with fabric.Connection(pi_ip, user=pi_user, connect_kwargs={'password': pi_pswd}) as c:
                result = c.run('python ' + step_count_pi_path + ' ' + server_ip_addr)
                print(result)
        elif pi_type == "facial_rec":
            with fabric.Connection(pi_ip, user=pi_user, connect_kwargs={'password': pi_pswd}) as c:
                result = c.run('python ' + facial_rec_pi_path + ' ' + server_ip_addr)
                print(result)
        elif pi_type == "fall_detector":
            pass
        else:
            print("Error: Bad Handle")
            return

if __name__ == "__main__":
    main1()

    
