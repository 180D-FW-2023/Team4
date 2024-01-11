import socket
import numpy as np
from scipy.signal import find_peaks
from scipy.signal import savgol_filter
import multiprocessing 
import fabric
import subprocess

path = "./data/"
step_count_pi_path = "~/step_count_client_pi.py"

def main():
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Assigns a port for the server that listens to clients connecting to this port.
    serv.bind(('0.0.0.0', 8080))
    serv.listen(5)
    
    serv_ip_addr = subprocess.run(['ipconfig', 'getifaddr', 'en0'], stdout=subprocess.PIPE)
    serv_ip_addr = serv_ip_addr.stdout.decode()
    print("server ip adddress: " + serv_ip_addr)

    # TODO: order?
    # step count start pi client code
    step_count_info_list = None
    with open("step_count_pi_ip.txt") as file_step_count:
        step_count_info_list = file_step_count.read().splitlines() 
    # TODO: error handling
    assert(len(step_count_info_list) == 3)
    p0 = multiprocessing.Process(target=run_pi, args=(step_count_info_list, serv_ip_addr ))
    p0.start()

    while True:
        conn, addr = serv.accept()
        print("client connection ip address: " + addr[0])
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
    
    y_smooth = savgol_filter(accel_mag, window_length=40, polyorder=3, mode="nearest")
    smooth_peaks, _ = find_peaks(y_smooth, height=0.2)

    total_peaks = len(smooth_peaks)

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

def run_pi(info, server_ip_addr):
    pi_ip = info[0]
    pi_user = info[1]
    pi_pswd = info[2]
    with fabric.Connection(pi_ip, user=pi_user, connect_kwargs={'password': pi_pswd}) as c:
        result = c.run('python ' + step_count_pi_path + ' ' + server_ip_addr)
        print(result)

if __name__ == "__main__":
    main()

    
