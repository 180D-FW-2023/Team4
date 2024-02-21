import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import altair as alt
from datetime import date
from datetime import timedelta
import os
import calendar
import numpy as np

st_autorefresh(interval=1000, key="dataframerefresh")

# with open('steps.txt','r') as f:
#    my_set = f.read().splitlines()

# if len(my_set) >= 1:
#     s = my_set[0]
# else:
#     s = 0

# st.title("Today's Step Count: " + s)

hours = []
today = date.today()
today_step = 0

if os.path.exists("step_count/data/"+ str(today) + "_total.csv"):
    with open("step_count/data/"+ str(today) + "_total.csv", "r") as f:
        day_steps = f.readlines()
        for steps in day_steps:
            steps = steps.split(",")
            hour = steps[0]
            hour_steps = steps[1]
            if hour != "total":
                hours.append(hour_steps)
            else:
                today_step = hour_steps
else:
    day_steps = "total"
    for i in range(24):
        hours.append(0)

st.title("Today's Step Count: " + str(today_step))

"Hourly Step Count"
source = pd.DataFrame({
    'Steps': hours,
    'Hour': ['12-1 AM', '1-2 AM', '2-3 AM', '3-4 AM', '4-5 AM', '5-6 AM', '6-7 AM', '7-8 AM', '8-9 AM', '9-10 AM', '10-11 AM', '11 AM-12 PM', 
              '12-1 PM', '1-2 PM', '2-3 PM', '3-4 PM', '4-5 PM', '5-6 PM', '6-7 PM', '7-8 PM', '8-9 PM', '9-10 PM', '10-11 PM', '11 PM-12 AM']
    })

bar_chart = alt.Chart(source).mark_bar().encode(
    y='Steps:Q',
    x=alt.X('Hour', type='ordinal', sort=None)
)

st.altair_chart(bar_chart, use_container_width=True)

days = []
days_steps = []

for i in range(7):
    today_minus = today - timedelta(days = i)
    if os.path.exists("step_count/data/"+ str(today_minus) + "_total.csv"):
        with open("step_count/data/"+ str(today_minus) + "_total.csv", "r") as f:
            day_step = int(f.readline().rstrip().split(",")[1])
            weekday = calendar.day_name[today_minus.weekday()]
            days.append(weekday)
            # days.append(str(today_minus))
            days_steps.append(day_step)
    else:
        weekday = calendar.day_name[today_minus.weekday()]
        days.append(weekday)
        # days.append(str(today_minus))
        days_steps.append(0)

days.reverse()
days_steps.reverse()

st.title("Average Daily Step Count for Past 7 Days: " + str(round(np.average(days_steps))))

"Daily Step Count"
source2 = pd.DataFrame({
    'Steps': days_steps,
    'Day': days
    })

bar_chart2 = alt.Chart(source2).mark_bar().encode(
    y='Steps:Q',
    x=alt.X('Day', type='ordinal', sort=None)
)

st.altair_chart(bar_chart2, use_container_width=True)