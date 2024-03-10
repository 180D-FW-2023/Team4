import streamlit as st
from streamlit_autorefresh import st_autorefresh
import ast
from PIL import ImageFile
from pages.Output import sidebar_status
ImageFile.LOAD_TRUNCATED_IMAGES = True
from st_pages import show_pages_from_config, add_page_title

add_page_title()

# show_pages_from_config()
st.subheader("Use the current frames to focus the camera")

st_autorefresh(interval=1000, key="dataframerefresh")

st.image('gui_txt_files/test.png', caption='Current Frame')