import streamlit as st
import subprocess
import sys
import os

def on_click():
    subprocess.call(['python','server.py'])

st.button('Click to run server', on_click=on_click)