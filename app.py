import streamlit as st
import datetime
import requests
from streamlit_folium import st_folium
import folium

'''
# TaxiFareModel front
'''

st.markdown('''
# Estimate your taxi fare''')

columns_date =  st.columns(2)
date = columns_date[0].date_input(
    "Travel date:",
    datetime.date(2024,5,31))
time = columns_date[1].time_input(
    "Travel time:",
    datetime.time(19,18,00))
#st.write('Travel date:', d)

DEFAULT_LATITUDE = 40.783282
DEFAULT_LONGITUDE = -73.950655
m = folium.Map(location=[DEFAULT_LATITUDE, DEFAULT_LONGITUDE], zoom_start=10)

f_map = st_folium(m, width=725, height=500, returned_objects=['last_clicked'])

selected_latitude = DEFAULT_LATITUDE
selected_longitude = DEFAULT_LONGITUDE

if f_map['last_clicked']:
    selected_latitude = f_map["last_clicked"]["lat"]
    selected_longitude = f_map["last_clicked"]["lng"]
st.text(selected_latitude)
st.text(selected_longitude)
columns = st.columns(2)
pickup_lon = columns[0].number_input('Pickup longitude', value=-73.950655)
pickup_lat = columns[1].number_input('Pickup latitude', value= 40.783282)
dropoff_lon = columns[0].number_input('Dropoff longitude', value= -73.984365)
dropoff_lat = columns[1].number_input('Dropoff latitude', value= 40.769802)
nb_passengers = columns[0].number_input('Number of passengers', value= 2)


url = 'https://taxifare.lewagon.ai/predict'


def call_api():
    params = {
            "pickup_datetime" : str(date)+" "+str(time),
            "pickup_longitude" :  pickup_lon,
            "pickup_latitude" : pickup_lat,
            "dropoff_longitude" :  dropoff_lon,
            "dropoff_latitude" : dropoff_lat,
            "passenger_count" : nb_passengers,
        }
    print(params)
    return requests.get(url, params=params).json()['fare']

if st.button('click me'):
    # print is visible in the server output, not in the page
    response = call_api()
    st.text(f"réponse: {response}")
