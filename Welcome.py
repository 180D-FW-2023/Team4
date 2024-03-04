import streamlit as st
import os
import streamlit as st
from PIL import Image
from pages.Output import sidebar_status

cwd = os.getcwd()
cwd = cwd[:cwd.find('Team4') + 5]
os.chdir(cwd)
from pages.Output import sidebar_status


st.title('Welcome to MemoryMate')

st.session_state['fall'] = 'Never'

image = Image.open('gui_txt_files/logo.png')

st.image(image)
sidebar_status()