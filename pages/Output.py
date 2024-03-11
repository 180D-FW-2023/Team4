import streamlit as st
import subprocess
import sys
import os
import time
from streamlit_autorefresh import st_autorefresh
from PIL import ImageFile
from datetime import date
from st_pages import show_pages_from_config, add_page_title

add_page_title()

# show_pages_from_config()

ImageFile.LOAD_TRUNCATED_IMAGES = True
# cwd = os.getcwd()
# path = cwd[:cwd.find('Team4') + 5]

# sys.path.append('../Team4')
st_autorefresh(interval=1000, key="dataframerefresh")

def sidebar_status():
    with open('gui_txt_files/server.txt','r') as f_obj:
        s = f_obj.read()
        status = "🔴"
        if (s == "good"):
            status = "🟢"
        elif(s == "eh"):
            status = "🟡"
        st.sidebar.text("Server Status: " + status)

    with open('gui_txt_files/face_recog_camera_status.txt','r') as f_obj:
        s = f_obj.read().rstrip()
        if (s == "up"):
            st.sidebar.text("Camera Status: " + "🟢")
        else:
            st.sidebar.text("Camera Status: " + "🔴")

    with open("gui_txt_files/step_count_status.txt", 'r') as f:
        sc_status = f.read().rstrip()

    if sc_status == "up":
        st.sidebar.text("Step Count Status: 🟢")
    else:
        st.sidebar.text("Step Count Status: 🔴")

    with open('gui_txt_files/face_recog_status.txt', 'r') as f:
        fr_status = f.read().rstrip()

    if fr_status == "up":
        st.sidebar.text("Facial Recognition Status: 🟢")
    else:
        st.sidebar.text("Facial Recognition Status: 🔴")

sidebar_status()
# with open('gui_txt_files/fall.txt','r') as f:
#     my_set = f.read().splitlines()

# #f_time = "Never"
# if len(my_set) >= 1:
#     s = my_set[0]
# else:
#     s = 0
# if s == "fall":
#     t = time.localtime()
#     current_time = time.strftime("%H:%M:%S", t)
#     f_time = current_time
#     with open('gui_txt_files/falls.txt', 'w') as f:
#         f.write(str(f_time))

try:
    st.image('gui_txt_files/out.png', caption='Recognized Face')
except:
    pass

today = date.today()
today_step = 0

if os.path.exists("step_count/data/"+ str(today) + "_total.csv"):
    with open("step_count/data/"+ str(today) + "_total.csv", "r") as f:
        today_step = int(f.readline().rstrip().split(",")[1])

st.title("Today's Step Count: " + str(today_step))

with open('gui_txt_files/fall_time.txt', 'r') as f:
    my_set = f.read().splitlines()
st.title("Last Fall: " + my_set[0])
#st.dataframe(my_set, column_config={"value": "Last Fall"}, use_container_width = True)
#on_click()