import streamlit as st
import ultraimport

ssh = ultraimport('__dir__/../../ssh.py', 'main1')

user = st.text_input('Username')
pwd = st.text_input('Password')
hname = st.text_input('Hostname', 'raspberrypi.local')
pi = st.selectbox('Which Pi?', ('step_count', 'facial_recognition', 'Fall Detection'))

st.button('Click to Run', on_click = ssh, args = (user, pwd, pi, hname))