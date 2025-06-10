import numpy as np
import pandas as pd
import streamlit as st
import preprocesser
import pyarrow
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy
df = pd.read_csv('Athlete_Event.csv')
region_df = pd.read_csv('noc_regions.csv')


df = preprocesser.preprocess(df, region_df)

st.sidebar.title("Olympic Data Analysis")
st.sidebar.image('olympic_logo.png')
user_menu = st.sidebar.radio('Select an option', ('Medal Tally', 'Overall Analysis', 'Country-wise analysis', 'Athlete-wise analysis'))


if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select year", years)
    selected_country = st.sidebar.selectbox("Select country", country)
    medal_tally = helper.fetch_medal_tally(df,selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall tally')

    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal tally in '+str(selected_year) + ' in olympics')

    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title('Overall performance of '+selected_country)

    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title("performance of" + selected_country + ' in year '+str(selected_year))

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    st.title('Top statistics')
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('cities')
        st.title(cities)

    with col3:
        st.header('sports')
        st.title(sports)
    col4, col5, col6 = st.columns(3)
    with col4:
        st.header('Events')
        st.title(events)

    with col5:
        st.header('athletes')
        st.title(athletes)

    with col6:
        st.header('nations')
        st.title(nations)

    st.title('participating nations over the years')
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.plotly_chart(fig)

    st.title('Events over the years')
    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.plotly_chart(fig)

    st.title('Athletes over the years')
    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x="Edition", y="Name")
    st.plotly_chart(fig)

    st.title("No. of events over time(Every sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
                annot=True)
    st.pyplot(fig)

    st.title("Most successful athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a sport ', sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)


if user_menu == 'Country-wise analysis':
    st.sidebar.title('Country-wise analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('select country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sport")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))

    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title("top 10 athletes of " +selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)
if user_menu == 'Athlete-wise analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)

    st.title("Distibution of age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a sport ', sport_list)

    temp_df = helper.Weight_V_Height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'])
    st.title('Height vs Weight')
    st.pyplot(fig)

    st.title('Men vs Women participation over the years')
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    st.plotly_chart(fig)