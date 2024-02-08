# API Flight Prices data extraction + analysis project
# Research question:
# When is the best moment to book a flight from Valencia-Amsterdam?
# - How do flight prices develop over the year? -> Are there differences or patterns noticeable at monthly/weekly/daily level?
# - Is the amount of time prior to the flight of influence on the price?

import pandas as pd
import requests
import plotly.express as px

# Flight calendar with all flight prices and dates, based on flight destination, without airlines
# For comparison flight prices per date
url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/getPriceCalendar"

querystring = {"originSkyId": "VLC", "destinationSkyId": "AMS", "fromDate": "2021-01-01"}

headers = {
    "X-RapidAPI-Key": "1e0d4b7f19mshc21672d5cc2b7d3p1e127ajsn754648442b38",
    "X-RapidAPI-Host": "sky-scrapper.p.rapidapi.com"
}

# Retrieve data and change format
response = requests.get(url, headers=headers, params=querystring)
data = response.json()
results = data.get('data').get('flights').get('days')

# Create empty list to save results
parsed_data = []

# Loop over dictionary in list
for dictionary in results:
    date = dictionary['day']
    category = dictionary['group']
    price = dictionary['price']
    parsed_data.append([date, category, price])

# Create dataframe with flight data in columns
column_names = ['date', 'group', 'price']
df = pd.DataFrame(parsed_data, columns=column_names)

# Convert datatype of date column to datetime
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year.astype('Int64')
df['month'] = df['date'].dt.month.astype('Int64')
df['day'] = df['date'].dt.day.astype('Int64')
df['weekday'] = df['date'].dt.weekday

# Replace integer values of weekdays by strings
df['weekday'] = df['weekday'].astype(str)
df['weekday_text'] = df['weekday'].str.replace('0', 'monday').str.replace('1', 'tuesday').str.replace('2', 'wednesday').str.replace('3', 'thursday').str.replace('4', 'friday').str.replace('5', 'saturday').str.replace('6', 'sunday')

# Replace string values of groups by integers
df['group_num'] = df['group'].str.replace('high', '2').str.replace('medium', '1').str.replace('low', '0')
df['group_num'] = df['group_num'].astype('Int64')


# Create new dataframe with variables we'd like to know correlation of
df_c = df[['group_num', 'price', 'year', 'month', 'day', 'weekday']]

# Calculate correlation coefficient for all combinations of variables
data_corr = df_c.corr().round(3)

# Show scores in heatmap for overview
px.imshow(data_corr).show()

# Prior knowledge:
# Correlation >=0.7 and <0.9 means there is a strong relationship between the variables.
# Correlation >=0.5 and <0.7 means there is a moderate relationship  between the variables.
# Correlation >=0.3 and <0.5 means there is a weak relationship between the variables.
# Correlation <0.3 means there is no relationship between the variables.

# Findings: ..........
