import fabric

# wired connection and return ip addr of pi

def main(user, pswd, pi_name):
    with fabric.Connection("raspberrypi.local", user=user, connect_kwargs={'password': pswd}) as c:
        # gets the ip address of the pi for future communication
        result = c.run("ip -4 a")
        result = str(result)
        # TODO: error handle
        result = result[result.find("wlan0:"):]
        pi_ip = result[result.find("inet") + 5:result.find("/")]
        # stores ip address of pi, username, and password
        file = open(pi_name + "_pi_ip.txt", "w")
        file.write(pi_ip + "\n" + user + "\n" + pswd + "\n")
        file.close()
        # puts the correct script onto the pi
        # TODO: add to background of rc?
        if pi_name == "step_count":
            c.put("./step_count_client_pi.py")
        elif pi_name == "face_recognition":
            pass
        elif pi_name == "fall_detection":
            pass
        else:
            # TODO: error handle
            pass
        # TODO: pi installlation with pip

if __name__ == "__main__":
    # TODO: username and password input
    # TODO: password store securely
    main("pi", "isabella", "step_count")
