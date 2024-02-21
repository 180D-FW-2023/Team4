import socket
from scipy.signal import find_peaks
from scipy.signal import savgol_filter
import multiprocessing 
import subprocess
import os
from pathlib import Path
import time
from socket import SHUT_RDWR

import io
import struct
import cv2 as cv
import numpy as np
from face_recog.detector import recognize_faces
import fabric
import scrypt
import paramiko


cwd = os.getcwd()
cwd = cwd[:cwd.find('Team4') + 5]

path = cwd + "/step_count/data/"
step_count_pi_path = "./step_count_client_pi.py"
facial_rec_pi_path = "./facial_rec_client_pi.py"

names = []
total_seen = set()
nice_pi_name = {
  "step_count": "Step Count",
  "facial_rec": "Face Recognition",
  "fall_detect": "Fall Detection"
}

def main1():
    try: 
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Assigns a port for the server that listens to clients connecting to this port.
        serv.bind(('0.0.0.0', 8080))
        serv.listen(5)
    except:
        print("Please Try Again. Server is not properly starting up.")
        return

    # TODO: only on mac?
    serv_ip_addr = subprocess.run(['ipconfig', 'getifaddr', 'en0'], stdout=subprocess.PIPE)
    serv_ip_addr = serv_ip_addr.stdout.decode()
    print("server ip adddress: " + serv_ip_addr)

    p3 = multiprocessing.Process(target=server_fall)
    p3.start()

    # gets step counter pi info
    step_count_info_list = None
    try:
        with open("step_count_pi_ip.txt") as file_step_count:
            step_count_info_list = file_step_count.read().splitlines() 
            b = bytes.fromhex(step_count_info_list[-1])
            step_count_info_list[-1] = scrypt.decrypt(b, 'password')
    except:
         print("Error: Set Up Your Step Counter Pi")
    else:
        if(len(step_count_info_list) != 3):
            print("Error: Set Up Your Step Counter Pi Again")
        else:
            # step count start pi client code
            p0 = multiprocessing.Process(target=run_pi, args=(step_count_info_list, serv_ip_addr, "step_count" ))
            p0.start()

    # facial rec start pi client code
    facial_rec_info_list = None
    try:
        with open("facial_rec_pi_ip.txt") as file_facial_rec:
            facial_rec_info_list = file_facial_rec.read().splitlines()
            b = bytes.fromhex(facial_rec_info_list[-1])
            facial_rec_info_list[-1] = scrypt.decrypt(b, 'password')    
    except:
         print("Error: Set Up Your Facial Recognition Pi")
    else:
        if(len(facial_rec_info_list) != 3):
            print("Error: Set Up Your Facial Recognition Pi Again")
        else: 
            p01 = multiprocessing.Process(target=run_pi, args=(facial_rec_info_list, serv_ip_addr, "facial_rec" ))
            p01.start()

    # fall detection start pi client code
    fall_detect_info_list = None
    try:
        with open("fall_detect_pi_ip.txt") as file_fall_detect:
            fall_detect_info_list = file_fall_detect.read().splitlines() 
            b = bytes.fromhex(fall_detect_info_list[-1])
            fall_detect_info_list[-1] = scrypt.decrypt(b, 'password')
    except:
         print("Error: Set Up Your Fall Detector Pi")
    else:
        if(len(fall_detect_info_list) != 3):
            print("Error: Set Up Your Fall Detector Pi Again")
        else:
            # step count start pi client code
            p02 = multiprocessing.Process(target=run_pi, args=(fall_detect_info_list, serv_ip_addr, "fall_detect" ))
            p02.start()

    # if no known ip adddresses exist, stop
    if step_count_info_list is None and facial_rec_info_list is None:
            return

    while True:
        conn, addr = serv.accept()
        print("client connection ip address: " + addr[0])
        # if unknown client, don't accept tcp connections
        if (step_count_info_list is None or addr[0] != step_count_info_list[0]) and (facial_rec_info_list is None or addr[0] != facial_rec_info_list[0]):
            conn.shutdown(SHUT_RDWR)
            conn.close()
            print('Unknown Client Disconnected')
            continue
        first_message = conn.recv(4096).decode('utf_8')
        if (first_message == "step count"):
            print("Step Counter Pi Starting")
            p1 = multiprocessing.Process(target=server_step_count, args=(conn, ))
            p1.start()
        if (first_message == "face recognition"):
            print("Facial Recognition Pi Starting")
            p2 = multiprocessing.Process(target=server_face_rec, args=(conn, ))
            p2.start()
        
def convert_strings_to_floats(x_in, y_in, z_in):
    xdata = []
    ydata = []
    zdata = []
    iterator_len = min(len(x_in), len(y_in), len(z_in))
    for i in range(iterator_len):
        try:
            x_float = float(x_in[i])
            y_float = float(y_in[i])
            z_float = float(z_in[i])
            xdata.append(x_float)
            ydata.append(y_float)
            zdata.append(z_float)
        except:
            pass
    output_array = [xdata, ydata, zdata]
    return output_array

def step_count(data):
    if data.ndim < 2:
        return 0
    
    out_data = convert_strings_to_floats(data[:,2], data[:,3], data[:,4])
    xdata = out_data[0]
    ydata = out_data[1]
    zdata = out_data[2]

    accel_mag = np.sqrt((np.power(xdata, 2) + np.power(ydata, 2) + np.power(zdata, 2)))
    accel_mag = accel_mag - np.mean(accel_mag)
    
    y_smooth = savgol_filter(accel_mag, window_length=40, polyorder=3, mode="nearest")
    smooth_peaks, _ = find_peaks(y_smooth, height=0.2)

    total_peaks = len(smooth_peaks)

    return total_peaks

def step_count_update(data, day_step_count_prev_hours, conn, current_date, current_hour):
    hour_step_count = step_count(data)
    cur_step_count = day_step_count_prev_hours + hour_step_count
    print("Step Count: " + str(cur_step_count))
    # with open(cwd + '/steps.txt', 'w') as f:
    #     f.write(str(cur_step_count))
    send_data = str(cur_step_count) + ";"
    conn.sendall(send_data.encode())
    file_total = file_open(path + current_date + "_total.csv", "r")
    totals = file_total.readlines()
    file_total.close()
    file_total = file_open(path + current_date + "_total.csv", "w")
    for line in totals:
        hour = line.split(",")[0]
        if hour == "total":
            file_total.write("total," + str(cur_step_count) + "\n")
        elif hour == current_hour:
            file_total.write(hour + "," + str(hour_step_count) + "\n")
        elif hour.isdigit() and int(hour) <= 23 and int(hour) >= 0:
            file_total.write(line)
    file_total.close()

def server_step_count(conn):
    current_date = ""
    current_hour = ""
    day_step_count_prev_hours = 0

    file_name = None
    file = None
    conn.settimeout(20)
    p0 = None
    try:
        while True:
            data = conn.recv(4096)
            if not data: break
            list_data = data.decode('utf_8').replace("\n", "").split(";")
            for item in list_data: 
                list_item = item.split(",")
                bad = False
                for i in range(len(list_item)):
                    # if one of values is not there
                    if list_item[i] is None or list_item[i] == "":
                        bad = True
                        break
                    # if accelerometer data
                    if i == 2 or i == 3 or i == 4:
                        if list_item[i] == '-':
                            bad = True
                            break
                if bad == True:
                    continue
                if len(list_item) != 5:
                    continue
                if len(list_item[0]) != 10:
                    continue
                if list_item[1][2] != ":" or list_item[1][5] != ":":
                    continue

                if file_name and file and (p0 is None or not p0.is_alive()):
                    file.close()
                    try:
                        data = np.genfromtxt(file_name, delimiter =',', dtype = str, invalid_raise = False)
                    except:
                        print("Please Try Again. Data not being stored properly.")
                    if p0 is not None:
                        if not p0.is_alive():
                            p0.join()
                            p0 = multiprocessing.Process(target=step_count_update, args=((data, day_step_count_prev_hours, conn, current_date, current_hour)))
                            p0.start()
                    else:
                        p0 = multiprocessing.Process(target=step_count_update, args=((data, day_step_count_prev_hours, conn, current_date, current_hour)))
                        p0.start()
                    file = file_open(file_name, "a")

                # in current date and hour
                if list_item[0] == current_date and list_item[1][0:2] == current_hour:
                    if file:
                        file.write(item + "\n")
                # in current date, new hour
                # TODO: test this!!
                elif list_item[0] == current_date and list_item[1][0:2] != current_hour:
                    if file:
                        file.close()
                    current_hour = list_item[1][0:2]
                    file_name = path + current_date + "_" + current_hour + ".csv"
                    file = file_open(file_name, "a")
                    file.write(item + "\n")
                # in new date/just started
                else:
                    if file:
                        file.close()
                    current_date = list_item[0]
                    current_hour = list_item[1][0:2]
                    file_name = path + current_date + "_" + current_hour + ".csv"
                    file = file_open(file_name, "a")
                    file.write(item + "\n")
                    # TODO: error handle/test
                    # if starting again
                    if p0 is not None:
                        p0.join()
                    if os.path.exists(path + current_date + "_total.csv"):
                        file_total = file_open(path + current_date + "_total.csv", "r")
                        totals = file_total.readlines()
                        # get the total step count
                        total = int(totals[0].split(",")[1])
                        # get step count for current hour
                        hour_total = int(totals[int(current_hour)+1].split(",")[1])
                        day_step_count_prev_hours = total - hour_total
                        file_total.close()
                    # if in new date/started for first time this day
                    else:
                        file_total = file_open(path + current_date + "_total.csv", "w")
                        file_total.write("total,0\n")
                        for i in range(24):
                            file_total.write(str(i)+",0\n")
                        file_total.close()
                        day_step_count_prev_hours = 0
    except Exception as e:
        print(type(e))
        print(e)
        conn.shutdown(SHUT_RDWR)
        conn.close()
        print('Step Count Server Disconnected Socket')

def file_open(file_name, type):
    try: 
        file = open(file_name,type)
        return file
    except:
        dir = file_name[:file_name.rfind("/")]
        Path(dir).mkdir(parents=True, exist_ok=True)
        return file_open(file_name)

def server_fall():
    subprocess.call(['sh', cwd + '/fall_detection/shell_script_new.sh'])

def server_face_rec(conn):
    connection = conn.makefile('rb')
    conn.settimeout(20)

    try:
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
            message = ''
            for name in names_recognized:
                if name not in total_seen:
                    total_seen.add(name)
                    message += name
                    message += ', '
            if len(total_seen) != 0:
                with open(cwd + '/total_seen.txt', 'w') as f:
                    f.write(str(total_seen))
            #print("I passed")
            encodedMessage = bytes(message, 'utf-8')
            conn.sendall(encodedMessage)
            #print("I passed")
    except Exception as e:
        print(type(e))
        print(e)
        conn.shutdown(SHUT_RDWR)
        conn.close()
        print('Facial Recognition Client Disconnected')

def run_pi(info, server_ip_addr, pi_type):
    pi_ip = info[0]
    p0 = multiprocessing.Process(target=start_pi_code, args=(info, server_ip_addr, pi_type ))
    p0.start()

    while True:
        time.sleep(1)
        # if the pi is down
        if not ping_test(pi_ip):
            print(pi_type + ": ping down")
            # if the run pi script is going
            if p0 is not None and p0.is_alive():
                p0.terminate()
                p0.join()
                print("Your " + nice_pi_name[pi_type] + " Pi is Down")
        # if the pi is up
        else:
            print(pi_type + ": ping up")
            # if the running pi code process is not running
            # was down and coming back up
            if p0 is not None and not p0.is_alive():
                print("Your " + nice_pi_name[pi_type] + " Pi is Coming Back Up")
                p0 = multiprocessing.Process(target=start_pi_code, args=(info, server_ip_addr, pi_type ))
                p0.start()

def start_pi_code(info, server_ip_addr, pi_type):
    pi_ip = info[0]
    pi_user = info[1]
    pi_pswd = info[2]

    try:
        if pi_type == "step_count":
            with fabric.Connection(pi_ip, user=pi_user, connect_kwargs={'password': pi_pswd}) as c:
                result = c.run('python ' + step_count_pi_path + ' ' + server_ip_addr)
        elif pi_type == "facial_rec":
            with fabric.Connection(pi_ip, user=pi_user, connect_kwargs={'password': pi_pswd}) as c:
                result = c.run('python ' + facial_rec_pi_path + ' ' + server_ip_addr)
        elif pi_type == "fall_detect":
            with fabric.Connection(pi_ip, user=pi_user, connect_kwargs={'password': pi_pswd}) as c:
                result = c.run("./subscriber/bin/simple_publisher")
        else:
            print("Error: Bad Handle")
            return
    except (TimeoutError, paramiko.ssh_exception.AuthenticationException):
        print("Error: Please Run the Setup on Your " + nice_pi_name[pi_type] + " Pi Again")
    except Exception as e:
        print(type(e))
        print(e)

def ping_test(ip):
    num = 10
    response = os.popen(f"ping -c {num} {ip} ").read()
    count = response.count("Request timeout") + response.count("Request timed out.")
    if count >= num-1:
        return False
    return True

if __name__ == "__main__":
    main1()