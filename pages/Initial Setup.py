import streamlit as st
import ultraimport
import os
from ssh import main1
from st_pages import show_pages_from_config, add_page_title
import fabric
import paramiko
import socket
import subprocess
add_page_title()

show_pages_from_config()

#ssh = ultraimport('__dir__/../../ssh.py', 'main1')
cwd = os.getcwd()
print('setup' + cwd)

def ssh(user, pswd, pi_name, host_name, windows):
    try:
        with fabric.Connection(host_name, user=user, connect_kwargs={'password': pswd}) as c:
            result = c.run("ip -4 a")
            result = str(result)
            result = result[result.find("wlan0:"):]
            pi_ip = result[result.find("inet") + 5:result.find("/")]
            if pi_name == "step_count":
                c.put("./pi_code/step_count_client_pi.py")
            elif pi_name == "facial_rec":
                c.put("./pi_code/facial_rec_client_pi.py")
            elif pi_name == "fall_detect":
                if (windows):
                    s = "pscp -pw \"" + pswd + "\" ./fall_detection/subscriber/* "+user+"@"+pi_ip+":/subscriber"
                else:
                    s = "sshpass -p \"" + pswd + "\" scp -r ./fall_detection/subscriber "+user+"@"+pi_ip+":"
                subprocess.run(s, shell=True)
                c.run("make -C subscriber clean")
                c.run("make -C subscriber bin")
                c.run("make -C subscriber bin/simple_publisher")
            else:
                pass
            st.success('Succesfully Uploaded!', icon="✅")
    except paramiko.ssh_exception.AuthenticationException:
        st.warning('Authentication Failed: Username or Password Wrong', icon="🚨")
    except TimeoutError:
        st.warning('Timed Out. Check Your Hostname is Correct and Try Again', icon="🚨")
    except socket.gaierror:
        st.warning('Check Your Raspberry Pi is Plugged in Properly (Data Port) and Hostname is Correct.\nIf you just plugged your Raspberry Pi in, it takes about a minute to boot up before you can do setup', icon="🚨")
    except Exception as e:
        st.warning("Error Occurred. Please Try Again", icon="🚨")

user = st.text_input('Username')
pwd = st.text_input('Password', type="password")
hname = st.text_input('Hostname', 'raspberrypi.local')
pi = st.selectbox('Which Pi?', ('Step Counter', 'Facial Recognition', 'Fall Detection'))
windows = st.checkbox("I'm on Windows")

if pi == 'Step Counter':
    pi = 'step_count'

elif pi == 'Facial Recognition':
    pi = 'facial_rec'

elif pi == 'Fall Detection':
    pi = 'fall_detect'

st.button('Click to Run', on_click = ssh, args = (user, pwd, pi, hname, windows))
