import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import webbrowser
from PIL import Image
import plotly.express as px
import time

st.markdown('# All About Boston Home Page')
st.sidebar.markdown('# All About Boston Home Page')
def main_page():
    st.markdown("# All About Boston Home Page")
    st.sidebar.markdown("# All About Boston Home Page")
def page2():
    st.markdown("# Time for Crime")
    st.sidebar.markdown("# Time for Crime")

st.write('# Boston Crime Incident Reports 2021')
st.sidebar.header('Filter: ')
crime_df = pd.read_csv('boston_crime2022.csv')

image1= image2 = Image.open('boston_pic.png')
st.image(image1, caption='City of Boston')

st.subheader(
    "The data used for this app was gained from the use of Analyze Boston, specifically the 2021 Crime Incident Reports dataset available on their website. \n"
    "Please select Analyze Boston below to be redirected to the source:"
)

link = '[Analyze Boston](https://data.boston.gov/dataset/crime-incident-reports-august-2015-to-date-source-new-system)'
st.markdown(link, unsafe_allow_html=True)

if st.checkbox('Preview Raw Data'):
    st.subheader('2021 Boston Crime Incidents Raw Data')
    st.write(crime_df)

st.markdown("In the original dataset the police districts are referenced as their letter and number identifier. \n"
            "To make the information within the dataset more interpretable to users the identier has been \n"
            "altered to the full name of that police district as it is recognized within the City of Boston. \n"
            )

dict = {"A1":"Downtown", 'A7': "East Boston", "B2":"Roxbury", "B3":"Mattapan", "A15":"Charlestown", "C6": "South Boston",
                                   "C11": "Dorchester",
                                   "D4":"South End",
                                   "D14": "Brighton",
                                   "E5": "West Roxbury",
                                   "E13": "Jamaica Plains",
                                   "E18": "Hyde Park",
                                   "null": "Unrecorded",
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

tab1,tab2,tab3= st.tabs(['Review of 2021','Shooting Related Incidents','Mapping'])

with tab1:
    st.markdown("Crime Reports by District in 2021")
    bar= alt.Chart(crime_df_2,title='# of Incidents Reported in 2021 by District').mark_bar(color= '#c7293b').encode(
        alt.Y("DISTRICT",title= "Police District",sort='-x'),
        alt.X('count()',title="Number of Incidents")
    )
    st.altair_chart(bar, use_container_width=True)
    st.subheader('More About the Top 3 Overall Crime Report Districts')
    st.text(
        "Based on the crime reports for 2021 the police department district with the \n"
        "most reported incidents was identified as B2 commonly known as Roxbury. \n"
    )

    link_rox = '[Find out more about Roxbury - Boston, MA Demographics](https://www.areavibes.com/boston-ma/roxbury/demographics/)'
    st.markdown(link_rox, unsafe_allow_html=True)
    link_south = '[Find out more about South End - Boston, MA Demographics](https://www.areavibes.com/boston-ma/south+end/demographics/)'
    st.markdown(link_south, unsafe_allow_html=True)
    link_dorch = '[Find out more about Dorchester - Boston, MA Demographics](https://www.areavibes.com/boston-ma/south+dorchester/demographics/)'
    st.markdown(link_dorch,unsafe_allow_html=True)

    st.subheader('Learn more about what offenses were the highest reported, use the filter on the right to adjust:')
    
    with st.spinner('Loading...'):
        time.sleep(6)
    st.success('Updated')

    bar2= alt.Chart(filtered_df, title='Incident Offense Count 2021').mark_bar(color= '#c7293b').encode(
        alt.Y("OFFENSE_DESCRIPTION",title= "Offense of Incident",sort='x'),
        alt.X('count()',title="Number of Incidents")
    )
    st.altair_chart(bar2, use_container_width=True)

with tab2: 
    st.header("Weapons of Mass[achusetts] Destruction?")
    image2 = Image.open('guns.png')
    st.image(image2)
    st.subheader('Boston Gun Related Incident Reports')

    link_guns = '[Boston Gun Laws and Guidelines](https://www.boston.gov/owning-firearm-boston)'
    st.markdown(link_guns,unsafe_allow_html=True)

    shooting_only= filtered_df[filtered_df['SHOOTING']==1]
    Shooting_district = shooting_only.groupby('DISTRICT').count()

    Shooting_df = shooting_only.groupby('OFFENSE_DESCRIPTION')['SHOOTING'].count()

    st.subheader('Shooting Count Based on Offenses Reported within 2021')
    
    with st.spinner('Mapping your selection...'):
        time.sleep(6)
    st.success('Updated')

    shooting_bar2 = alt.Chart(shooting_only).mark_bar().encode(
        alt.X("OFFENSE_DESCRIPTION",title= "Incident Offense",sort='-y'),
        alt.Y('SHOOTING',title="Shootings")
    )
    st.altair_chart(shooting_bar2, use_container_width=True)

    Shooting_df2 = shooting_only.drop(shooting_only[shooting_only['lon'] == 0].index)
    st.subheader('The below map represents shooting related incidents reported in 2021 for the filtered district.')
    st.map(Shooting_df2)


with tab3:
    st.header("Districts Incident Report Mapping Boston, MA 2021")
    
    map_crime = filtered_df.drop(filtered_df[filtered_df['lon'] == 0].index)

    st.map(map_crime)
    
    with st.spinner('Mapping...'):
        time.sleep(6)
    st.success('Updated')

    st.subheader("IMPORTANT NOTE: \n"
                "There are some instances where the report filed location coordinates may have been recorded inaccurately \n"
                "or another situation caused reports to be received via the Boston Police Department from off the coast of Africa at longitude 0 degrees. \n"
                "The City of Boston is a coastal location and some reports may reflect incident reports requiring water rescue and response in combination \n"
                "with the United States Coast Guard based in Boston, MA. \n"
                "It is also important to note that not all incident calls logged for a given district took place within that district based upon the recorded address.\n")

st.subheader(
        "To find out more about the City of Boston and its Police Department a direct link to the source can be found below.\n"
    )

link2 = '[City of Boston Police Department](https://www.boston.gov/departments/police)'
st.markdown(link2, unsafe_allow_html=True)

#contact form only worked locally and did not work when streamlit published
#st.subheader('Receive updates from the City of Boston PD by entering name and email below.')

#contact_form= """
#<form action="https:formsubmit.co/kanncolby@gmail.com" method="POST">
    #<input type="text" name= "name" placeholder="Full Name" required>
    #<input type="email" name="email" placeholder="Email Address" required>
    #<button type="submit">Send</button>
#</form>
#"""

#st.markdown(contact_form, unsafe_allow_html=True)

#st.text('**Due to this app being an example it does not submit info entered above \n' 
        #'to the City of Boston PD Relations Team email address. The existing app uses \n'
        #'an email address the app builder had to act as a placeholder to show this section \n' 
        #'would work if the email were altered to a different one within the underlying code.**\n')
