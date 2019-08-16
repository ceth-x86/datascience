import numpy as np
from sklearn.datasets import make_blobs

import urllib
import json
import datetime
import calendar
from os import path
from collections import Counter

JSON_FILE = 'weather.json'

if not path.exists(JSON_FILE):
    data_url = 'https://data.townofcary.org/api/v2/catalog/datasets/rdu-weather-history/exports/json'

    urllib.request.urlretrieve(data_url, JSON_FILE)

f = open(JSON_FILE, 'r')
lines = f.readlines()
f.close()
json_data = ''.join(lines)

weather = json.loads(json_data)

weather_by_date = {}

for day in weather:
  dt = datetime.datetime.strptime(day['date'], '%Y-%m-%d')
  if dt.year < 2019:
    if not dt.year in list(weather_by_date.keys()):
      weather_by_date[dt.year] = {}
    if not dt.month in weather_by_date[dt.year].keys():
      weather_by_date[dt.year][dt.month] = []
    weather_by_date[dt.year][dt.month].append(day)
    
flatten = lambda l: [item for sublist in l for item in sublist]

MONTHS = np.array([calendar.month_abbr[m] for m in (np.arange(12) + 1)])

def monthly_data_by_key(month=1, key='precipitation'):
  monthly_data = flatten([weather_by_date[year][month] for year in weather_by_date.keys()])
  return [day[key] for day in monthly_data]

def data_by_key(year=2018, key='precipitation'):
    return flatten([weather_by_date[year][month] for month in np.arange(1, 13)])

def monthly_data_values_by_key(month=1, key='precipitation'):
  monthly_data = flatten([weather_by_date[year][month] for year in weather_by_date.keys()])
  return [day[key] for day in monthly_data]

def monthly_freq_counts(month=1, key='precipitation'):
    data = np.array(monthly_data_by_key(month=month, key=key))
    l_bound = np.min(data)
    u_bound = np.max(data)
    intervals = np.linspace(l_bound, u_bound, 11)
    freq = Counter()
    
    for point in data:
        for index, interval in enumerate(intervals):
            if point < interval:
                freq[index] += 1
                break
    
    return [freq[key] for key in sorted(freq.keys())]

def precip_sums_for_year(year=2018):
  if year not in sorted(list(weather_by_date.keys())):
    raise IndexError('Invalid year')
  weather_for_year = weather_by_date[year]
  return sorted(zip(weather_for_year.keys(), [sum([day['precipitation'] for day in weather_for_year[month]]) for month in weather_for_year.keys()]))

def temps_by_month_for_year(year=2018):
    if year not in sorted(list(weather_by_date.keys())):
        raise IndexError('Invalid year')
    the_weather = weather_by_date[year]
    the_weather = dict(zip(sorted(the_weather.keys()), [[day['temperaturemax'] for day in the_weather[month]]  for month in sorted(the_weather.keys())]))
    for key in the_weather.keys():
        if len(the_weather[key] < 31):
            the_weather[key]
    

def get_wind_points():
    avg_wind = monthly_data_by_key(month=1, key='avgwindspeed')
    fast_wind = monthly_data_by_key(month=1, key='fastest5secwindspeed')
    
    points = list(zip(avg_wind, fast_wind))
    points = np.array([point for point in points if point[0] is not None and point[1] is not None])
    for _ in range(5):
        mindex = np.argmax(points[:,1])
        points = np.delete(points, mindex, 0)
    return points

def get_blobs():
    return make_blobs(n_samples=200, centers=5)

def get_normal_counts(n_samples=10000):
    data = np.random.randn(n_samples)
    freq = Counter()
    
    l_bound = np.min(data)
    u_bound = np.max(data)
    intervals = np.linspace(l_bound, u_bound, 21)
    
    for point in data:
        for index, interval in enumerate(intervals):
            if point < interval:
                freq[index] += 1
                break
                
    return [freq[key] for key in sorted(freq.keys())]
    
    