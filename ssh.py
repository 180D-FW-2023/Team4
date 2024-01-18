import fabric

# wired connection and return ip addr of pi

def main1(user, pswd, pi_name, host_name):
    with fabric.Connection(host_name, user=user, connect_kwargs={'password': pswd}) as c:
        result = c.run("ip -4 a")
        result = str(result)
        # TODO: error handle
        result = result[result.find("wlan0:"):]
        pi_ip = result[result.find("inet") + 5:result.find("/")]
        file = open("/Users/Home/Team4/" + pi_name + "_pi_ip.txt", "w")
        file.write(pi_ip + "\n" + user + "\n" + pswd + "\n")
        file.close()
        if pi_name == "Step Count":
            c.put("/Users/Home/Team4/step_count/step_count_client_pi.py")
        elif pi_name == "Face Recognition":
            c.put("/Users/Home/Team4/stream_client.py")
        elif pi_name == "Fall Detection":
            pass
        else:
            # TODO: error handle
            pass

if __name__ == "__main__":
    main1("pi", "krisha", "step_count", "raspberrypi.local")
