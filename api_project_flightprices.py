# API Flight Prices data extraction + analysis project
# Research question:
# When is the best moment to book a flight from Valencia-Amsterdam?
# - How do flight prices develop over the year? -> Are there differences or patterns noticeable at monthly/weekly/daily level?
# - Is the amount of time prior to the flight of influence on the price?

import config
import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.express as px

# Flight calendar with all flight prices and dates, based on flight destination, without airlines
# For comparison flight prices per date
url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/getPriceCalendar"
querystring = {"originSkyId": "VLC", "destinationSkyId": "AMS", "fromDate": "2024-01-01"}
headers = {"X-RapidAPI-Key": config.api_key, "X-RapidAPI-Host": config.api_host}

# Retrieve data from API and parsing text
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

# Create a dataframe with columns
column_names = ['date', 'group', 'price']
df = pd.DataFrame(parsed_data, columns=column_names)


# Now the data is retrieved, let's start cleaning the data
# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Split column into year, month, and day
df['year'] = df['date'].dt.year.astype('Int64')
df['month'] = df['date'].dt.month.astype('Int64')
df['day'] = df['date'].dt.day.astype('Int64')

# Additionally, add weekdays
df['weekday'] = df['date'].dt.weekday

# Replace integer values of weekdays by text
df['weekday'] = df['weekday'].astype(str)
df['weekday_text'] = df['weekday'].str.replace('0', 'monday').str.replace('1', 'tuesday').str.replace('2', 'wednesday').str.replace('3', 'thursday').str.replace('4', 'friday').str.replace('5', 'saturday').str.replace('6', 'sunday')
df['weekday'] = df['weekday'].astype('Int64')

# Replace values of group column by integers
df['group_num'] = df['group'].str.replace('high', '2').str.replace('medium', '1').str.replace('low', '0')
df['group_num'] = df['group_num'].astype('Int64')


# Checking distribution and outliers for 'price' column
df.boxplot('price')
# plt.show()

# Create new variables with average group score per month, day, weekday
group_month = df.groupby('month')['group_num'].value_counts()

# Plot results in bar chart for better overview
px.bar(group_month, barmode='group', labels='group_num').show()
# Adding more charts here...........

# Calculating correlation between variables
# Create new dataframe with variables we'd like to know correlation of
df_c = df[['group_num', 'price', 'year', 'month', 'day', 'weekday']]

# Calculate correlation coefficient for all combinations of variables
data_corr = df_c.corr().round(3)

# Show scores in heatmap for overview
px.imshow(data_corr).show()
# Findings: There is a strong correlation between the variables 'price' and 'group', as expected, as they indicated the price range. No further correlations found.

# TO DO:
# - Adjust current chart
# - Add more charts for rest of variables
# - Answer RQ part 1
