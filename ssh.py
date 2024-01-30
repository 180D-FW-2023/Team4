import fabric
import paramiko
import socket

# wired connection and return ip addr of pi

def main1(user, pswd, pi_name, host_name):
    try:
        file = None
        # TODO: connection fails
        with fabric.Connection(host_name, user=user, connect_kwargs={'password': pswd}) as c:
            result = c.run("ip -4 a")
            result = str(result)
            # TODO: error handle
            result = result[result.find("wlan0:"):]
            pi_ip = result[result.find("inet") + 5:result.find("/")]
            if pi_name == "step_count":
                file = open("./" + pi_name + "_pi_ip.txt", "w")
                # TODO: move put to server?
                c.put("./step_count_client_pi.py")
            elif pi_name == "facial_rec":
                file = open("./" + pi_name + "_pi_ip.txt", "w")
                c.put("./facial_rec_client_pi.py")
            elif pi_name == "Fall Detection":
                pass
            else:
                # TODO: error handle
                pass
            if file:
                file.write(pi_ip + "\n" + user + "\n" + pswd + "\n")
                file.close()
            else:
                # TODO: error handle
                pass
    except paramiko.ssh_exception.AuthenticationException:
        print("Error: Authentication Failed: Username or Password Wrong")
    except TimeoutError:
        print("Error: Timed Out. Check Your Hostname is Correct and Try Again")
    except socket.gaierror:
        print("Error: Check Your Raspberry Pi is Plugged in and Hostname is Correct.")
        print("If you just plugged your Raspberry Pi in, it takes about a minute to boot up before you can do setup")
    except Exception as e:
        print(type(e))
        print(e)

if __name__ == "__main__":
    main1("pi", "isabella", "step_count", "raspberrypi.local")
