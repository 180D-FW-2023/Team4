import socket
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

path = "./data/"

def main():
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Assigns a port for the server that listens to clients connecting to this port.
    serv.bind(('0.0.0.0', 8080))
    serv.listen(5)
    file = None

    while True:
        conn, addr = serv.accept()
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

    # accel_mag = accel_mag - np.mean(accel_mag)
    # min_peak_height = 2*np.std(accel_mag) + np.mean(accel_mag)
    # TODO: tune height, make greater of 1.3 and std dev?
    peaks, _ = find_peaks(accel_mag, height=1.3)

    return len(peaks)

if __name__ == "__main__":
    main()

    
