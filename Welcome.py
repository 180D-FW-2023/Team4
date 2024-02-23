import streamlit as st
import os
cwd = os.getcwd()
cwd = cwd[:cwd.find('Team4') + 5]
os.chdir(cwd)
print(cwd)


st.title('Welcome to MemoryMate')

st.session_state['fall'] = 'Never'



