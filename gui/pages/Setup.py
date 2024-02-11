import streamlit as st
import ultraimport
import os
import datetime
from ssh import main1

#ssh = ultraimport('__dir__/../../ssh.py', 'main1')
cwd = os.getcwd()
print('setup' + cwd)

user = st.text_input('Username')
pwd = st.text_input('Password', type="password")
hname = st.text_input('Hostname', 'raspberrypi.local')
pi = st.selectbox('Which Pi?', ('Step Counter', 'Facial Recognition', 'Fall Detection'))

if pi == 'Step Counter':
    pi = 'step_count'

elif pi == 'Facial Recognition':
    pi = 'facial_rec'

elif pi == 'Fall Detection':
    pi = 'fall_detect'

st.button('Click to Run', on_click = main1, args = (user, pwd, pi, hname))

if os.path.exists('step_count_pi_ip.txt'):
    mtime = os.path.getmtime('step_count_pi_ip.txt')
    mtime = datetime.datetime.fromtimestamp(mtime)
    st.text("Step Count Setup Last Updated: " + str(mtime))
else:
    st.text("Step Count Not Yet Setup")

if os.path.exists('facial_rec_pi_ip.txt'):
    mtime = os.path.getmtime('facial_rec_pi_ip.txt')
    mtime = datetime.datetime.fromtimestamp(mtime)
    st.text("Facial Recognition Setup Last Updated: " + str(mtime))
else:
    st.text("Facial Recognition Not Yet Setup")