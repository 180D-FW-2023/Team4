import socket
from datetime import datetime
import numpy as np


def main():
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Assigns a port for the server that listens to clients connecting to this port.
    serv.bind(('0.0.0.0', 8080))
    serv.listen(5)

    

    while True:
        conn, addr = serv.accept()
        print(addr)
        first_message = conn.recv(4096).decode('utf_8')
        if (first_message == "step count"):
            data_points = 0
            list_time = []
            while True:
                data = conn.recv(4096)
                if not data: break
                list_data = data.decode('utf_8').replace("\n", "").split(";")

                for item in list_data: 
                    list_item = item.split(",")
                    if len(list_item) != 5:
                        continue
                    data_points += 1
                    send_time = datetime.strptime(list_item[1], "%H:%M:%S.%f")
                    now = datetime.now()
                    time = now.strftime("%H:%M:%S.%f")
                    cur_time = datetime.strptime(time, "%H:%M:%S.%f")
                    time_delta = send_time-cur_time
                    print(time_delta)
                    list_time.append(time_delta)
                
                if (data_points >= 2000):
                    np_time = np.array(list_time)
                    print("Average Latency: " + str(np.mean(np_time)))
                    break
            conn.close()
            print('client disconnected')
        

if __name__ == "__main__":
    main()

    
