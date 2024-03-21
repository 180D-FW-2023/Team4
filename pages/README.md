# Code Organization
This directory contains TODO: krisha

## Files
The purpose of each file will be explained below
- `Bluetooth Headphone Connection.py`: 
- `Email Setup.py`: a page where you can add the emails you want the fall detector to send messages to upon a fall
   - Sources:
      - checkbox: https://discuss.streamlit.io/t/dynamically-created-multiple-checkbox/18273
      - email validation: https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
   - Decisions: We decided to allow and implement the ability to subscribe multiple emails to fall detection messages
   - Future Improvements: Send a confirmation email that the email address is subsribed to
- `Fall Detection.py`: 
- `Focus Camera.py`: 
- `Initial Setup.py`: a page where you can upload code onto your plugged in pi
    - Sources:
      - fabric ssh: https://www.fabfile.org
   - Decisions: We decided to not have this page used before every setup but instead only if your pi is wiped and you need to put code back on it.
   - Future Improvements: Add a section that updates the rc.local
- `Load Facial Recognition Data.py`: 
- `Output.py`: 
 - Sources:
      - sidebar: https://docs.streamlit.io/library/api-reference/layout/st.sidebar
   - Decisions:
   - Future Improvements: 
- `Recognized Face.py`: 
- `Run Server.py`: 
- `Step Count.py`: a page where the current and weekly step count data is displayed
   - Sources:
      - bar chart: https://blog.finxter.com/bar-charts-learning-streamlit-with-bar-charts/
   - Decisions: We wanted to display the day's worth of data and the week's worth of data which required changing how server stores data.
   - Future Improvements: Add month worth of data to display