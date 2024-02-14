import streamlit as st
import subprocess
import sys
import os
import time
from streamlit_autorefresh import st_autorefresh
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
# cwd = os.getcwd()
# path = cwd[:cwd.find('Team4') + 5]

# sys.path.append('../Team4')
st_autorefresh(interval=1000, key="dataframerefresh")

with open('fall.txt','r') as f:
   my_set = f.read().splitlines()

#f_time = "Never"
if len(my_set) >= 1:
    s = my_set[0]
else:
    s = 0
if s == "fall":
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    f_time = current_time
    with open('falls.txt', 'w') as f:
        f.write(str(f_time))

try:
    st.image('out.png', caption='Recognized Face')
except:
    pass

with open('steps.txt','r') as f:
   my_set = f.read().splitlines()

if len(my_set) >= 1:
    s = my_set[0]
else:
    s = 0

st.title("Current Step Count: " + s)

with open('falls.txt', 'r') as f:
    my_set = f.read().splitlines()
st.title("Last Fall: " + my_set[0])
#st.dataframe(my_set, column_config={"value": "Last Fall"}, use_container_width = True)
#on_click()