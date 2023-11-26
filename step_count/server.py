import socket

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
                    current_hour = item[1][1]
                    file_name = path + current_date + "_" + current_hour + ".csv"
                    file = open(file_name,"w")
                # in new date
                else:
                    file.close()
                    current_date = item[0]
                    current_hour = item[1][1]
                    file_name = path + current_date + "_" + current_hour + ".csv"
                    file = open(file_name,"w")
        conn.close()
        print('client disconnected')

if __name__ == "__main__":
    main()

    
