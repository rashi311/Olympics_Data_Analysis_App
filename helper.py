import pandas as pd
import pyarrow
import numpy as np

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'Games', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
    return medal_tally


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'Games', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x

def data_over_time(df, col):
    temp_df = df.drop_duplicates(['Year', col])
    data = temp_df.groupby('Year')[col].nunique().reset_index()
    data.rename(columns={'Year': 'Edition', col: col}, inplace=True)
    return data



def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country

def most_successful(df,sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15)
    x.rename(columns={'count': 'Medals'}, inplace=True)
    x = x.merge(df[['Name', 'Sport', 'region']], on='Name', how='left').drop_duplicates('Name')

    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    x = temp_df['Name'].value_counts().reset_index().head(10)
    x.rename(columns={'count': 'Medals'}, inplace=True)
    #x = x.merge(df, on='Name')[['Name', 'Medals', 'Sport']].drop_duplicates('Name')
    x = x.merge(df[['Name', 'Sport', 'region']], on='Name', how='left').drop_duplicates('Name')
    return x


def Weight_V_Height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region']).copy()
    athlete_df['Medal'] = athlete_df['Medal'].fillna('No Medal')
    '''
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    '''
    if sport!='Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    Men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    Women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = Men.merge(Women, on="Year", how='left')
    final.fillna(0, inplace=True)
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    return final



