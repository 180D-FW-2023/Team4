import streamlit as st
import subprocess
import sys
import os

def on_click():
    subprocess.call(['python','server.py'])

def on_click_kill():
    with open('gui_txt_files/server.txt','w') as f_obj:
        f_obj.write("bad")
    subprocess.call(['pkill','-f','subscriber'])
    subprocess.call(['pkill','-f','shell_script_new'])
    subprocess.call(['pkill','-f','multiprocessing.spawn'])
    subprocess.call(['pkill','-f','server.py'])
    subprocess.call(['pkill','-f','subscriber'])

st.button('Click to run server', on_click=on_click)
st.button('Stop server', on_click=on_click_kill)
