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

    while True:
        conn, addr = serv.accept()
        from_client = ''

        current_date = ""
        current_hour = ""
        day_step_count = 0

        while True:
            data = conn.recv(4096)
            if not data: break
            from_client += data.decode('utf_8')
            list_data = data.decode('utf_8').replace("\n", "").split(";")
            for item in list_data: 
                if len(item.split(",")) != 5:
                    continue
                print(item)
                # in current date and hour
                if item[0] == current_date and item[1][1] == current_hour:
                    file.write(item + "\n")
                # in current date, new hour
                elif item[0] == current_date and item[1][1] != current_hour:
                    file.close()
                    # TODO: make this a new process so parallelism
                    day_step_count += step_count(file_name)
                    print("Current Stepp Count: " + day_step_count)
                    current_hour = item[1][1]
                    file_name = path + current_date + "_" + current_hour + ".csv"
                    file = open(file_name,"w")
                # in new date
                else:
                    file.close()
                    # TODO: store step count data
                    day_step_count = 0
                    current_date = item[0]
                    current_hour = item[1][1]
                    file_name = path + current_date + "_" + current_hour + ".csv"
                    file = open(file_name,"w")
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

    # TODO: change height
    # accel_mag = accel_mag - np.mean(accel_mag)
    min_peak_height = np.std(accel_mag) + np.mean(accel_mag)
    peaks, _ = find_peaks(accel_mag, height=min_peak_height)

    return len(peaks)

if __name__ == "__main__":
    main()

    
