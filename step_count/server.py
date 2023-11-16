import socket
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Assigns a port for the server that listens to clients connecting to this port.
serv.bind(('0.0.0.0', 8080))
serv.listen(5)
while True:
    conn, addr = serv.accept()
    from_client = ''
    file = open('items.csv','w')

    while True:
        data = conn.recv(4096)
        if not data: break
        from_client += data.decode('utf_8')
        list_data = data.decode('utf_8').replace("\n", "").split(";")
        for item in list_data: 
            if len(item.split(",")) != 5:
                continue
            print(item)
            file.write(item + "\n")
    file.close()
    conn.close()
    print('client disconnected')