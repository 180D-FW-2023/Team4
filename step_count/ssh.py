import fabric

# wired connection and return ip addr of pi

def main(user, pswd, pi_name):
    with fabric.Connection("raspberrypi.local", user=user, connect_kwargs={'password': pswd}) as c:
        result = c.run("ip -4 a")
        result = str(result)
        # TODO: error handle
        result = result[result.find("wlan0:"):]
        pi_ip = result[result.find("inet") + 5:result.find("/")]
        file = open(pi_name + "_pi_ip.txt", "w")
        file.write(pi_ip + "\n" + user + "\n" + pswd + "\n")
        file.close()
        if pi_name == "step_count":
            c.put("./step_count_client_pi.py")
        elif pi_name == "face_recognition":
            pass
        elif pi_name == "fall_detection":
            pass
        else:
            # TODO: error handle
            pass

if __name__ == "__main__":
    main("pi", "isabella", "step_count")
