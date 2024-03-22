import streamlit as st
import subprocess
import sys
import os
from st_pages import add_page_title

add_page_title()

def on_click():
    subprocess.call(['python','server.py'])

def on_click_kill():
    with open('gui_txt_files/server.txt','w') as f_obj:
        f_obj.write("bad")
    with open('gui_txt_files/step_count_status.txt', 'w') as f:
        f.write("down\n")
    with open('gui_txt_files/face_recog_status.txt', 'w') as f:
        f.write("down\n")
    with open('gui_txt_files/face_recog_camera_status.txt', 'w') as f:
        f.write("down\n")
    subprocess.call(['pkill','-f','subscriber'])
    subprocess.call(['pkill','-f','shell_script_new'])
    subprocess.call(['pkill','-f','multiprocessing.spawn'])
    subprocess.call(['pkill','-f','server.py'])
    subprocess.call(['pkill','-f','subscriber'])

st.button('Click to run server', on_click=on_click)
st.button('Stop server', on_click=on_click_kill)
