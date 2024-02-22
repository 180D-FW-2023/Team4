import subprocess
import streamlit as st
import os
#import pandas as pd
#from io import StringIO

# uploaded_files = st.file_uploader("Upload 5-10 Images", type=['png', 'jpg'], accept_multiple_files = True)

# for i in uploaded_files:
#     # To read file as bytes:
#     bytes_data = i.getvalue()
#     st.write("filename: ", i.name)
#     st.write(bytes_data)

    # with open(i.name, "wb") as binary_file:
    #     binary_file.write(bytes_data)

uploaded_files = st.file_uploader("Upload 5-10 Images", type=['png', 'jpg'], accept_multiple_files=True)

name = st.text_input("Name")

filepath = "./face_recog/training/" + name
if not os.path.exists(filepath):
    os.mkdir(filepath)

def on_click(filepath, uploaded_files):
    for i in uploaded_files:
        bytes_data = i.getvalue()
        i_name = filepath + "/" + i.name
        i_name = i_name.replace(" ", "_")
        with open(i_name, "wb") as binary_file:
            binary_file.write(bytes_data)

def on_click_train():
    subprocess.run(["python", "face_recog/detector.py", "--train"])
    

st.button("Upload files", on_click = on_click, args = (filepath, uploaded_files))

st.button("Retrain", on_click = on_click_train)

