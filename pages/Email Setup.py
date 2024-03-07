import streamlit as st
from streamlit_autorefresh import st_autorefresh
from pages.Output import sidebar_status
import os
from email_validator import validate_email, EmailNotValidError
from st_pages import show_pages_from_config, add_page_title

add_page_title()

# show_pages_from_config()

def update_email(email, email_list):
    try:
      if email in email_list:
          st.warning('Email Already Entered', icon="⚠️")
          return
      # validate and get info
      v = validate_email(email)
      with open('gui_txt_files/email.txt','a') as f:
        f.write(str(email)+"\n")
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        st.warning('Email Entered Not Valid', icon="🚨")

email_list = []

if os.path.exists('gui_txt_files/email.txt'):
    with open('gui_txt_files/email.txt','r') as f:
        email_list_pre = f.readlines()
    for email in email_list_pre:
        email = email.rstrip()
        if email != "":
            email_list.append(email)

if len(email_list) == 0:
    st.header("No Emails Reporting To")

email_add = st.text_input('Add Email')

st.button('Submit', on_click = update_email, args = (email_add,email_list,))

def remove_selected(selected_checks, email_list):
    for i in selected_checks:
        try:
            email_list.remove(i)
        except:
            pass
    with open('gui_txt_files/email.txt','w') as f:
        for i in email_list:
            f.write(i + '\n')

def checkbox_container(data):
    st.header('Subscribed Emails')
    cols = st.columns(2)
    if cols[0].button('Select All'):
        for i in data:
            st.session_state['dynamic_checkbox_' + i] = True
        st.rerun()
    if cols[1].button('Unselect All'):
        for i in data:
            st.session_state['dynamic_checkbox_' + i] = False
        st.rerun()
    for i in data:
        st.checkbox(i, key='dynamic_checkbox_' + i)
    email_add = get_selected_checkboxes()
    st.button('Remove Selected Emails', on_click = remove_selected, args = (email_add,email_list,))

def get_selected_checkboxes():
    return [i.replace('dynamic_checkbox_','') for i in st.session_state.keys() if i.startswith('dynamic_checkbox_') and st.session_state[i]]

if len(email_list) != 0:
    checkbox_container(email_list)

    