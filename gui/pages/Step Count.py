import streamlit as st
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=1000, key="dataframerefresh")

with open('steps.txt','r') as f:
   my_set = f.read().splitlines()

if len(my_set) >= 1:
    s = my_set[0]
else:
    s = 0

st.title("Current Step Count: " + s)