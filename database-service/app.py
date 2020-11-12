import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property  # fix for "ImportError: cannot import name 'cached_property'"

from cloudant import Cloudant
from flask import Flask
from flask_restplus import Api, Resource

import atexit

import os, sys


app = Flask(__name__)
api = Api(app,
          version='1.0.1',
          title='City Data Visualizer',
          default='API Endpoints',
          default_label='',
          doc='/apidocs/',
          prefix='/api')


# classes
@api.route('/api/v1/berlin-verschenken')
class BerlinVerschenken(Resource):
    def get(self):
        return get_table_data('berlin_verschenken'), 200


@api.route('/api/v1/berlin-shapes-district')
class BerlinShapesDistrict(Resource):
    def get(self):
        return get_table_data('berlin_shapes_district'), 200


@api.route('/api/v1/berlin-covid-district')
class BerlinCovidDistrict(Resource):
    def get(self):
        return get_table_data('berlin_covid_district'), 200


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


if __name__ == "__main__":
    # connect to db
    USER = os.environ.get('DB_USER')
    PASS = os.environ.get('DB_PW')
    URL = os.environ.get('DB_URL')
    client = Cloudant(USER, PASS, url=URL, connect=True, auto_renew=True)

    # run app
    app.run(debug=True)
