import fabric
import scrypt
import paramiko
import socket
import subprocess

# wired connection and return ip addr of pi

def main1(user, pswd, pi_name, host_name, windows):
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
                c.put("./pi_code/step_count_client_pi.py")
            elif pi_name == "facial_rec":
                file = open("./" + pi_name + "_pi_ip.txt", "w")
                c.put("./pi_code/facial_rec_client_pi.py")
            elif pi_name == "fall_detect":
                file = open("./" + pi_name + "_pi_ip.txt", "w")
                if (windows):
                    s = "pscp -pw \"" + pswd + "\" ./fall_detection/subscriber/* "+user+"@"+pi_ip+":/subscriber"
                else:
                    s = "sshpass -p \"" + pswd + "\" scp -r ./fall_detection/subscriber "+user+"@"+pi_ip+":"
                subprocess.run(s, shell=True)
                c.run("make -C subscriber clean")
                c.run("make -C subscriber bin")
                c.run("make -C subscriber bin/simple_publisher")
            else:
                # TODO: error handle
                pass
            if file:
                pwd = scrypt.encrypt(pswd, 'password')
                dec_pwd = pwd.hex()
                print(dec_pwd)
                file.write(pi_ip + "\n" + user + "\n" + dec_pwd + "\n")
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
    main1("pi", "jolin", "fall_detect", "raspberrypi.local")
