import os
import time
from typing import Optional

import requests
from flask import Flask
from flask_caching import Cache
from flask_pydantic import validate
from flask_restful import Api, Resource
from pydantic import BaseModel

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
app.cache = Cache(app)
api = Api(app)


# Validation classes
class ParametersChachedTemperatures(BaseModel):
    max: Optional[int] = os.environ.get('DEFAULT_MAX_NUMBER', 5)


# Rosources classes
class TemperatureByCity(Resource):
    @app.cache.cached(timeout=os.environ.get('CACHE_TLL', 300))
    @validate()
    def get(self, city_name: str):
        wheather_url = 'http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&appid={1}'

        # A api key should never be open in the code, but was provided to simplify the process and can only be used this way in development
        openweather_response = requests.get(wheather_url.format(city_name, os.environ.get('OPENWEATHER_APIKEY', '8006ee749a6b40a3235382082abb73c8'))).json()

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
    @validate()
    def get(self, query: ParametersChachedTemperatures):
        max_number = query.max
        keys = list(app.cache.cache._cache.keys())[:max_number]

        response = [app.cache.get(k) for k in keys if 'error' not in app.cache.get(k)]
        return response


api.add_resource(TemperatureByCity, '/temperature/<city_name>')
api.add_resource(Cached, '/temperature')

if __name__ == '__main__':
    app.run()
