import streamlit as st
import subprocess
import sys

# sys.path.append('../Team4')

def on_click():
    subprocess.call(['python','/Users/Home/Team4/server.py'])

st.button('Click to run server', on_click=on_click)
#on_click()