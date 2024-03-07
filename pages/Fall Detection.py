import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import ast
import time
from pages.Output import sidebar_status

st_autorefresh(interval=1000, key="dataframerefresh")

with open('gui_txt_files/fall.txt','r') as f:
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
    with open('gui_txt_files/falls.txt', 'w') as f:
        f.write(str(f_time))
with open('gui_txt_files/falls.txt', 'r') as f:
    my_set = f.read().splitlines()
st.dataframe(my_set, column_config={"value": "Last Fall"})

with open('gui_txt_files/gps.txt', 'r') as f:
    my_set = ast.literal_eval(f.read())

lat = my_set["best_lat"]
lon = my_set["best_lon"]

d = {'lat': [lat], 'lon': [lon]}
df = pd.DataFrame(d)

st.map(df)

sidebar_status()