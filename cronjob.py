#!/usr/local/bin/pipenv
import time
import requests
import queries
import json
# import concurrent.futures

cities = ['shanghai', 'houston', 'dallas', 'moscow', 'london', 'austin', 'washington', 'tokyo', 'paris', 'sydney', 'beijing', 'chicago', 'new york', 'los angeles', 'boston']
# cities = ['shanghai', 'boston']
def check_weather(city):
    session = queries.Session('postgresql://postgres@localhost:5432/weather_db')
    appid = '9ecc560e5c99c8be650566914f4192e6'
    url = 'http://api.openweathermap.org/data/2.5/weather'
    payload = {'q': city, 'appid': appid, 'units': 'imperial'}
    response = requests.get(url, params=payload)
    current_time = int(time.time())
    ts = time.localtime()
    fmt = '%Y-%m-%d %H:%M:%S'
    query_time = time.strftime(fmt, ts)
    session.query('''INSERT INTO weather_history VALUES
    (DEFAULT, %(city)s, %(contents)s, %(time)s, %(query_time)s)''', {'city': city, 'contents': json.dumps(response.json()), 'time': current_time, 'query_time': query_time})
    print(query_time)

# future_squirrel.py
 
# NUM_WORKERS = 4
 
# with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
#     futures = {executor.submit(check_weather, city.capitalize()) for city in cities}
#     concurrent.futures.wait(futures)

for city in cities:
    check_weather(city.capitalize())