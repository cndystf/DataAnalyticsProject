import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image

#read dataset
days_df = pd.read_csv("https://raw.githubusercontent.com/cndystf/DataAnalyticsProject/main/dashboard/cleaned_bikesharingdays.csv")
days_df['dteday'] = pd.to_datetime(days_df['dteday'])

#create several helper functions
def create_monthly_rents_df(df):
    monthly_rents_df=df.resample(rule='M', on='dteday').agg({
        "casual":"sum",
        "registered":"sum",
        "cnt":"sum"
    })
    monthly_rents_df.index=monthly_rents_df.index.strftime('%b-%y')
    monthly_rents_df=monthly_rents_df.reset_index()
    monthly_rents_df.rename(columns={
        "dteday":"monthyear",
        "cnt":"all_rents"
    }, inplace=True)
    return monthly_rents_df

def create_weekday_rents_df(df):
    weekday_rents_df=df.groupby("weekday").agg({
        "casual":"sum",
        "registered":"sum",
        "cnt":"sum"
    })
    weekday_rents_df=weekday_rents_df.reset_index()
    weekday_rents_df.rename(columns={
        "cnt":"all_rents"
    }, inplace=True)
    weekday_rents_df['weekday']= pd.Categorical(weekday_rents_df['weekday'], categories=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
    weekday_rents_df = weekday_rents_df.sort_values('weekday')
    return weekday_rents_df

def create_weather_rents_df(df):
    weather_rents_df=df.groupby("weathersit").agg({
        "casual":"sum",
        "registered": "sum",
        "cnt":"sum"
    })
    weather_rents_df=weather_rents_df.reset_index()
    weather_rents_df.rename(columns={
        "weathersit":"weather",
        "cnt":"all_rents"
    }, inplace=True)
    weather_rents_df['weather']=pd.Categorical(weather_rents_df['weather'], categories=['Clear/Partly Cloudy','Misty/Cloudy', 'Light Snow/Rain', 'Heavy Snow/Rain'])
    weather_rents_df=weather_rents_df.sort_values('weather')
    return weather_rents_df

def create_seasonal_rents_df(df):
    seasonal_rents_df=df.groupby("season").agg({
        "casual":"sum",
        "registered":"sum",
        "cnt":"sum"
    })
    seasonal_rents_df=seasonal_rents_df.reset_index()
    seasonal_rents_df.rename(columns={
           "cnt":"all_rents"
    }, inplace=True)
    seasonal_rents_df['season']= pd.Categorical(seasonal_rents_df['season'], categories=['Spring','Summer','Fall','Winter'])
    seasonal_rents_df = seasonal_rents_df.sort_values('season')
    return seasonal_rents_df

#make filter and sidebar dashboard
min_date=days_df["dteday"].min()
max_date=days_df["dteday"].max()

with st.sidebar:
    #image = Image.open('logo.jpeg') 
    st.image('logo.jpeg')

    start_date,end_date=st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = days_df[(days_df['dteday'] >= str(start_date)) & (days_df['dteday'] <= str(end_date))]

#assign to helper functions
monthly_rents_df = create_monthly_rents_df(main_df)
weekday_rents_df = create_weekday_rents_df(main_df)
weather_rents_df = create_weather_rents_df(main_df)
seasonal_rents_df = create_seasonal_rents_df(main_df)

#make dashboard mainpage
st.header("Bike Sharing Dashboard")

col1,col2,col3 = st.columns(3)

with col1:
    total_casual_rents = main_df['casual'].sum()
    st.metric("Casual Users", value=total_casual_rents)
with col2:
    total_registered_rents = main_df['registered'].sum()
    st.metric("Registered Users", value=total_registered_rents)
with col3:
    total_all_rents = main_df['cnt'].sum()
    st.metric("Total Users", value=total_all_rents)

color =['blue','green','orange']

#monthly
st.subheader("Monthly Rentals")

fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(
    monthly_rents_df['monthyear'],
    monthly_rents_df['all_rents']
)
ax.set_title("Number of Monthly Rentals in 2011-2012")
ax.set_ylabel("Total of Rents")
ax.set_xlabel("Date")
ax.tick_params(axis='both', labelsize=12)
st.pyplot(fig, use_container_width=True)

#weekday
st.subheader ("Weekday Rentals")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    x=weekday_rents_df['weekday'],
    y=weekday_rents_df['all_rents'],
    ax=ax
)
ax.set_title("Number of Weekday Rentals")
ax.set_ylabel("Total of Rents")
ax.set_xlabel("Day")
ax.tick_params(axis='both', labelsize=12)
st.pyplot(fig, use_container_width=True)

#weather
st.subheader('Rentals Based on Weather')
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    x=weather_rents_df['weather'],
    y=weather_rents_df['all_rents'],
    ax=ax
)
ax.set_title("Number of Rentals Based on Weather")
ax.set_ylabel("Total of Rents")
ax.set_xlabel("Weather")
ax.tick_params(axis='both', labelsize=12)
plt.ticklabel_format(style='plain', axis='y')
st.pyplot(fig, use_container_width=True)

#season
st.subheader('Rentals Based on Season')
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    x=seasonal_rents_df['season'],
    y=seasonal_rents_df['all_rents'],
    ax=ax
)
ax.set_title("Number of Rentals Based on Season")
ax.set_ylabel("Total of Rents")
ax.set_xlabel("Season")
ax.tick_params(axis='both', labelsize=12)
plt.ticklabel_format(style='plain', axis='y')
st.pyplot(fig, use_container_width=True)