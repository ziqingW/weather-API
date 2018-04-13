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
        print("it's main")
        self.render_template('main.html', {}) 
            
class HistoricHandler(TemplateHandler):
    def get(self):
        city = self.get_query_argument('city', None)
        records = self.session.query('''
        SELECT * FROM weather_history WHERE city=%(city)s ORDER BY time DESC LIMIT 5
        ''', {'city': city})
        self.render_template('historic.html', {'records': records, 'city': city})
        print("it's historic handler")
        
class SearchHandler(TemplateHandler):
         

            
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/search", SearchHandler),
        (r"/historic", HistoricHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler,
        {'path': 'api/static'})
        ], autoreload=True)
        
if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    app = make_app()
    app.listen(int(os.environ.get('PORT', '8080')))
    tornado.ioloop.IOLoop.current().start()

























        (r"/search", SearchHandler),