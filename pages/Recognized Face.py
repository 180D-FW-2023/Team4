import streamlit as st
from streamlit_autorefresh import st_autorefresh
import ast
from PIL import ImageFile
from pages.Output import sidebar_status
ImageFile.LOAD_TRUNCATED_IMAGES = True
from st_pages import show_pages_from_config, add_page_title

add_page_title()

show_pages_from_config()

st_autorefresh(interval=1000, key="dataframerefresh")

st.image('out.png', caption='Recognized Face')

with open('gui_txt_files/total_seen.txt','r') as f:
   my_set = ast.literal_eval(f.read())

st.dataframe(my_set, column_config={"value": "Faces Recognized"})
# st.json(my_set)
sidebar_status()