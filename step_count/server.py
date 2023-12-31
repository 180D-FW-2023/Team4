import socket
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import multiprocessing 
import fabric
import subprocess

path = "./data/"
step_count_pi_path = "~/Team4/step_count/acc_data_pi.py"

def main():
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Assigns a port for the server that listens to clients connecting to this port.
    serv.bind(('0.0.0.0', 8080))
    serv.listen(5)
    
    ip_addr = subprocess.run(['ipconfig', 'getifaddr', 'en0'], stdout=subprocess.PIPE)
    ip_addr = ip_addr.stdout.decode()
    print(ip_addr)

    # TODO: order? parallelize?
    p0 = multiprocessing.Process(target=run_pi, args=("raspberrypi.local", ip_addr, step_count_pi_path, ))
    p0.start()

    while True:
        conn, addr = serv.accept()
        print(addr)
        first_message = conn.recv(4096).decode('utf_8')
        if (first_message == "step count"):
            p1 = multiprocessing.Process(target=server_step_count, args=(conn, ))
            p1.start()
            # server_step_count(conn)
        
def convert_strings_to_floats(input_array):
    output_array = []
    for element in input_array:
        converted_float = float(element)
        output_array.append(converted_float)
    return output_array

def step_count(path_name):
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
    current_date = ""
    current_hour = ""
    day_step_count = 0

    hour_data = 0
    file_name = None
    file = None
    
    while True:
        data = conn.recv(4096)
        if not data: break
        list_data = data.decode('utf_8').replace("\n", "").split(";")

        for item in list_data: 
            list_item = item.split(",")
            if len(list_item) != 5:
                continue
            if len(list_item[0]) != 10:
                continue
            # print(item)
            # TODO: thread/process parallelize this
            # TODO: make it user input?
            hour_data += 1
            if file_name and hour_data % 50 == 0:
                file.close()
                cur_step_count = day_step_count + step_count(file_name)
                file = open(file_name,"a")
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
                file = open(file_name,"a")
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
                file = open(file_name,"a")
                file.write(item + "\n")
    conn.close()
    print('client disconnected')

def run_pi(pi_ip, ip_addr, script_path):
    with fabric.Connection(pi_ip, user="pi", connect_kwargs={'password': 'isabella'}) as c:
        result = c.run('python ' + script_path + ' ' + ip_addr)
        print(result)

if __name__ == "__main__":
    main()

    
