import streamlit as st
from streamlit_autorefresh import st_autorefresh
import time

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
    st.title("Last Fall At: " + f_time)

st.title("No Falls Yet")