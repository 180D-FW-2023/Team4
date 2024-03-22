import subprocess
import json
import plistlib
import streamlit as st
from st_pages import show_pages_from_config, add_page_title

add_page_title()

proc = subprocess.Popen(['system_profiler', '-xml', 'SPBluetoothDataType'], stdout=subprocess.PIPE)
output = proc.stdout.read()
pl = plistlib.loads(output)
devices = pl[0]['_items'][0]['device_not_connected']
dev_names = {}
for i in devices:
    for j in i.keys():
        dev_names[j] = i[j]['device_address']
st.dataframe(dev_names, column_config={"value": "MAC Address"})
name = st.selectbox('Select Device', dev_names)

def on_click():
    if (name == None):
        st.text("No device selected")
        return
    if (name not in dev_names):
        st.text("Invalid device")
    with open('gui_txt_files/bluetooth.txt', 'w') as f:
        f.write(name+"\n")
        f.write(dev_names[name])


st.button(label = "Save", on_click = on_click)