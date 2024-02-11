import streamlit as st
import subprocess
import sys
import os
from streamlit_autorefresh import st_autorefresh
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
# cwd = os.getcwd()
# path = cwd[:cwd.find('Team4') + 5]

# sys.path.append('../Team4')

def on_click():
    subprocess.call(['python','server.py'])

st.button('Click to run server', on_click=on_click)

st.image('out.png', caption='Recognized Face')

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