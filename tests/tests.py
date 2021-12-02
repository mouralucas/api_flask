import unittest
from app import app


class TemperatureByCityTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_city_temperature(self):
        cities = ['curitiba', 'london', 'munich', 'teresina', 'sao paulo', 'paris']

        for i in cities:
            response = self.app.get('/temperature/{0}'.format(i))

            # Check the response code
            self.assertEqual(200, response.status_code)

            # Check if all keys are in response
            self.assertIn('min', response.json)
            self.assertIn('max', response.json)
            self.assertIn('avg', response.json)
            self.assertIn('feels_like', response.json)
            self.assertIn('city', response.json)

        # Check the request when a parameter is passed
        response = self.app.get('/temperature?max=1')
        self.assertEqual(list, type(response.json))
        self.assertGreaterEqual(1, len(response.json))

        # Check the request without a parameter, using environ or DEFAULT_MAX_NUMBER
        response = self.app.get('/temperature')
        self.assertEqual(list, type(response.json))
        self.assertLessEqual(4, len(response.json))

    def test_edge_city_temperatures(self):
        cities = ['n', 'majspf', 46513645, ['asd', 'paris']]

        for i in cities:
            response = self.app.get('/temperature/{0}'.format(i))

            # Check the response code
            self.assertEqual(200, response.status_code)
            self.assertIn('error', response.json)


    def test_edge_cached(self):
        cities = ['curitiba', 'london', 'munich', 'teresina', 'sao paulo', 'paris']

        for i in cities:
            response = self.app.get('/temperature/{0}'.format(i))

        # Passing string as parameter
        response = self.app.get('/temperature?max=bsdf')
        self.assertEqual(400, response.status_code)
        self.assertIn('validation_error', response.json)
