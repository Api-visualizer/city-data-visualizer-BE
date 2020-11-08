from cloudant import Cloudant
from flask import Flask
from flask_restful import Resource, Api
from flasgger import Swagger, swag_from
import atexit

import os

app = Flask(__name__)

# swagger config
app.config['SWAGGER'] = {
    'title': 'City Data Visualizer',
    'uiversion': 3
}
swagger = Swagger(app)
api = Api(app)

# classes
class BerlinVerschenken(Resource):
    @swag_from('api.yml', validation=False)
    def get(self):
        return get_table_data('berlin_verschenken'), 200


class BerlinShapesDistrict(Resource):
    @swag_from('api.yml', validation=False)
    def get(self):
        return get_table_data('berlin_shapes_district'), 200


class BerlinCovidDistrict(Resource):
    @swag_from('api.yml', validation=False)
    def get(self):
        return get_table_data('berlin_covid_district'), 200


class Json(Resource):
    def get(self):
        return {'json sagt': 'hallo i bims der json'}, 200

# disconnct from db on server shutdown
@atexit.register
def shutdown():
    try:
        client.disconnect()
        print('disconnected from db')
    except Exception:
        pass


# fetch data from database
def get_table_data(table_name):
    try:
        table_data = client[table_name]
        payload = [data for data in table_data]
        return payload
    except Exception as e:
        print('ERROR: Could not fetch table {}. Cause: {}'.format(table_name, e))
        return ''


if __name__ == 'app':
    # register endpoints
    api.add_resource(BerlinVerschenken, '/api/v1/berlin-verschenken')
    api.add_resource(BerlinShapesDistrict, '/api/v1/berlin-shapes-district')
    api.add_resource(BerlinCovidDistrict, '/api/v1/berlin-covid-district')
    api.add_resource(Json, '/')

    # connect to db
    USER = os.environ.get('DB_USER')
    PASS = os.environ.get('DB_PW')
    URL = os.environ.get('DB_URL')
    client = Cloudant(USER, PASS, url=URL, connect=True, auto_renew=True)
    print(f'db client: {USER}, {PASS}, {URL}')
