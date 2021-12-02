import os
import time

import requests
from flask import Flask, request
from flask_caching import Cache
from flask_restful import Api, Resource


app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
app.cache = Cache(app)
api = Api(app)


# Rosources classes
class TemperatureByCity(Resource):
    @app.cache.cached(timeout=os.environ.get('CACHE_TLL', 300))
    def get(self, city_name: str):
        wheather_url = 'http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&appid={1}'

        openweather_response = requests.get(wheather_url.format(city_name, os.environ.get('OPENWEATHER_APIKEY'))).json()

        if openweather_response['cod'] == 200:
            response = {
                'min': openweather_response['main']['temp_min'],
                'max': openweather_response['main']['temp_max'],
                'avg': openweather_response['main']['temp'],
                'feels_like': openweather_response['main']['feels_like'],
                'city': {
                    'name': openweather_response['name'],
                    'country': openweather_response['sys']['country'],
                },
                'timestamp': time.ctime()
            }
        else:
            response = {'error': openweather_response['message']}

        return response


class Cached(Resource):
    def get(self):
        max_number = 5

        keys = list(app.cache.cache._cache.keys())[:max_number]

        response = [app.cache.get(k) for k in keys]
        return response


api.add_resource(TemperatureByCity, '/temperature/<city_name>')
api.add_resource(Cached, '/temperature')

if __name__ == '__main__':
    app.run()
