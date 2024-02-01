import streamlit as st
import subprocess
import sys
import os
# cwd = os.getcwd()
# path = cwd[:cwd.find('Team4') + 5]

# sys.path.append('../Team4')


def on_click():
    subprocess.call(['python','server.py'])

st.button('Click to run server', on_click=on_click)
#on_click()