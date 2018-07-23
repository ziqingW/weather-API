# weather-API
Weather Report is a simple app powered by Python Tornado and API from 'Openweathermap'. 

You can check the current weather condition of the searched city, or, list the historical queried results of the same city.

## Features
I designed multiple handlers for different scenarios to optimize API requests so as to improve efficiency
- If it's a search for new city, the API request will be called
- If the interval of query for the same city is less than 2 hours, the app will ask database for the latest result instead of making API request
- If the interval is longer than 2 hours, the API will be called and the latest results will be saved in database
___
## Nerd's thinking
### Gains:
- I created a cronjob in local to autoupdate the weather conditions of serveral main cities in the world every 1 hour
- However, such function was difficult to repeat when the app was deployed to Heroku
- I had to remove the autoupdate function for Heroku version for now, but definitely will come back to recover it in future

### Pains:
- Different conditions made the coding and debugging tiring
- Dealing with time zone and time format in database was really depressing

## Major Techs:
- Python
- Tornado
- Jinja2
- PostgreSQL

## Published:
[Heroku: Weather Report](https://miniweather.herokuapp.com/)
