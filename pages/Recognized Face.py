import streamlit as st
from streamlit_autorefresh import st_autorefresh
import ast
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

st_autorefresh(interval=1000, key="dataframerefresh")

st.image('out.png', caption='Recognized Face')

with open('total_seen.txt','r') as f:
   my_set = ast.literal_eval(f.read())

st.json(my_set)