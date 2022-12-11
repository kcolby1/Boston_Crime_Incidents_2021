import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import webbrowser
from PIL import Image
import time

st.markdown("# Time for Crime")
st.sidebar.markdown("# Time for Crime")
image3= Image.open('clock.png')
st.image(image3)
st.sidebar.header('Use the Below to Filter: ')

crime_df = pd.read_csv('boston_crime2022.csv')
dict = {"A1":"Downtown", 'A7': "East Boston", "B2":"Roxbury", "B3":"Mattapan", "A15":"Charlestown", "C6": "South Boston",
                                   "C11": "Dorchester",
                                   "D4":"South End",
                                   "D14": "Brighton",
                                   "E5": "West Roxbury",
                                   "E13": "Jamaica Plains",
                                   "E18": "Hyde Park",
                                   "N/A": "Unrecorded",
                                   "External": "Outside of Boston Districts"}

crime_df_2 = crime_df.replace({'DISTRICT' : dict})

crime_df_2 = crime_df_2.rename(columns={"Lat":"lat",
                                    "Long":"lon"})

district_list = ["Downtown", "East Boston", "Roxbury", "Mattapan", "Charlestown", "South Boston","Dorchester","South End",
                "Brighton","West Roxbury","Jamaica Plains","Hyde Park","Outside of Boston Districts"]

district_filter= st.sidebar.selectbox(
    'What district do you want to learn more about?',
    options=district_list,
    key='1'
)

if district_filter == "":
    filtered_df = crime_df_2
else:
    filtered_df = crime_df_2[crime_df_2['DISTRICT']== district_filter]

st.header("What Time Will Crime Strike in Your Neighborhood?")

with st.spinner('Tick, Tock, Tick, Tock...'):
    time.sleep(4)
st.success('Updated')

st.subheader('What hour are incidents most reported in your district?')
hour = alt.Chart(filtered_df, title= 'Incident Count by Hour').mark_line(color = '#CC6600').encode(
    alt.X("HOUR",title= "Hour of the Day"),
    alt.Y('count()', title='Number of Incidents')
)
st.altair_chart(hour, use_container_width=True)
st.text('Note: Hour 0 is the equivalent to midnight')

st.subheader('What day of the week are incidents most reported in your district?')
day = alt.Chart(filtered_df,title='Incident Count by Day').mark_bar(color='#CC6600').encode(
    alt.Y("DAY_OF_WEEK",title= "Day of the Week",sort='-x'),
    alt.X('count()', title='Number of Incidents')
)
st.altair_chart(day, use_container_width=True)
st.text("The overall busiest day of the week in Boston regarding incident reports in 2021 was \n"
        "Friday. The other days of the week followed closely behind.\n")

st.subheader('What month are incidents most reported in your district?')
month = alt.Chart(filtered_df,title='Incident Count by Month').mark_line(color = '#CC00CC').encode(
    alt.X("MONTH",title= "Month"),
    alt.Y('count()', title='Number of Incidents')
)
st.altair_chart(month, use_container_width=True)
