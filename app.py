import os
import time

import requests
from flask import Flask, request
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)

# Rosources classes
class TemperatureByCity(Resource):
    def get(self, city_name: str):
        wheather_url = 'http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&appid={1}'

        openweather_response = requests.get(wheather_url.format(city_name, os.environ.get('OPENWEATHER_APIKEY'))).json()

        return openweather_response


class Cached(Resource):
    def get(self):
        pass


api.add_resource(TemperatureByCity, '/temperature/<city_name>')
api.add_resource(Cached, '/temperature')

if __name__ == '__main__':
    app.run()
