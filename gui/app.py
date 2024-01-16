import streamlit as st
import subprocess
import sys

sys.path.append('../Team4')

def on_click():
    subprocess.call(['python','../server.py'])

st.button('Click me', on_click=on_click)
#on_click()



