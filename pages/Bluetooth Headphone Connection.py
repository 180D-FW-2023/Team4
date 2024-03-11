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
    # print(i)
    # print(type(i))
    for j in i.keys():
        dev_names[j] = i[j]['device_address']
st.dataframe(dev_names, column_config={"value": "MAC Address"})
name = st.selectbox('Select Device', dev_names)
    #dev_names.append()
#out = json.loads(output)   
#print(out)

# def checkbox_container(data):
#     st.header('Devices Found')
#     for i in data:
#         st.checkbox(i.name, key='dynamic_checkbox_' + i.name)

# def get_selected_checkboxes():
#     return [i.replace('dynamic_checkbox_','') for i in st.session_state.keys() if i.startswith('dynamic_checkbox_') and st.session_state[i]]

# if len(val_devices) != 0:
#     checkbox_container(val_devices)

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