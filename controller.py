import os
import tornado.ioloop
import tornado.web
import tornado.log
import time
import requests
import queries
import json

from jinja2 import \
  Environment, PackageLoader, select_autoescape
  
ENV = Environment(
  loader=PackageLoader('api', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
)

class TemplateHandler(tornado.web.RequestHandler):
    def render_template(self, tpl, context):
        template = ENV.get_template(tpl)
        self.write(template.render(**context))
    
    def get(self):
        self.set_header('Cache-Control', 'private')
        
    def initialize(self):
        self.session = queries.Session(
        'postgresql://postgres@localhost:5432/weather_db')
      
class MainHandler(TemplateHandler):
    def get(self):
        city = self.get_query_argument('city', None)
        current_time = int(time.time())
        search = self.get_query_argument('search', None)
        history = self.get_query_argument('history', None)
        if city:
            city = city.capitalize()
            if search:
                appid = os.environ.get('WEATHER_APP_ID')
                url = 'http://api.openweathermap.org/data/2.5/weather'
                payload = {'q': city, 'appid': appid, 'units': 'imperial'}
                ts = time.localtime()
                fmt = '%Y-%m-%d %H:%M:%S'
                query_time = time.strftime(fmt, ts)
                weather = self.session.query('''
                SELECT * FROM weather_history WHERE city=%(city)s ORDER BY time DESC''', {'city': city})
                if len(weather) > 0:
                    if current_time - weather[0]['time'] <= 900:
                        self.render_template('main_result.html', {'response': weather[0]['contents']})
                        print('database used', current_time)
                    elif 900 < current_time - weather[0]['time'] < 7200:
                        r = requests.get(url, params=payload)
                        print(json.dumps(r.json()))
                        self.render_template('main_result.html', {'response': r.json()})
                        self.session.query('''
                        UPDATE weather_history 
                        SET contents=%(contents)s, time=%(time)s, query_time=%(query_time)s WHERE city=%(city)s AND time=(SELECT max(time) from weather_history WHERE city=%(city)s)''',
                        {'city': city, 'contents': json.dumps(r.json()), 'time': current_time, 'query_time': query_time})
                        print('fetched new data and updated db', current_time)
                    else:
                        r = requests.get(url, params=payload)
                        self.render_template('main_result.html', {'response': r.json()})
                        self.session.query('''
                        INSERT INTO weather_history VALUES
                        (DEFAULT, %(city)s, %(contents)s, %(time)s, %(query_time)s)''',
                        {'city': city, 'contents': json.dumps(r.json()), 'time': current_time, 'query_time': query_time})
                        print('fetched new data and inserted new value', current_time)
                else:
                    r = requests.get(url, params=payload)
                    if r.json()['cod'] != 200:
                        self.render_template('error.html', {'city': city}) 
                    else:
                        self.render_template('main_result.html', {'response': r.json()})
                        self.session.query('''
                        INSERT INTO weather_history VALUES
                        (DEFAULT, %(city)s, %(contents)s, %(time)s, %(query_time)s)''',
                         {'city': city, 'contents': json.dumps(r.json()), 'time': current_time, 'query_time': query_time})
                        print('fetched new data, create new city', current_time)
            elif history:
                records = self.session.query('''
                SELECT * FROM weather_history WHERE city=%(city)s ORDER BY time DESC LIMIT 5
                ''', {'city': city})
                self.render_template('historic.html', {'records': records, 'city': city})
                print("it's historic handler")
        else:
            self.render_template('main.html', {}) 

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler,
        {'path': 'api/static'})
        ], reload=True)
        
if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    app = make_app()
    app.listen(int(os.environ.get('PORT', '8080')))
    tornado.ioloop.IOLoop.current().start()