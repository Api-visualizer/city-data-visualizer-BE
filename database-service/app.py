import os, sys

import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property  # fix for "ImportError: cannot import name 'cached_property'"

from cloudant import Cloudant
from flask import Flask
from flask_restplus import Api, Resource, reqparse

import atexit


app = Flask(__name__)
api = Api(app,
          version='1.0.1',
          title='City Data Visualizer',
          default='API Endpoints',
          default_label='',
          doc='/apidocs/')


# connect to db
USER = os.environ.get('DB_USER')
PASS = os.environ.get('DB_PW')
URL = os.environ.get('DB_URL')
client = Cloudant(USER, PASS, url=URL, connect=True, auto_renew=True)


# routes
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


@api.route('/api/v1/berlin-covid-district/latest')
class BerlinCovidDistrict(Resource):
    def get(self):
        return get_table_data_latest('berlin_covid_district'), 200


@api.route('/api/v1/berlin-accidents')
class BerlinCovidDistrict(Resource):
    def get(self):
        # Define parser and request args
        parser = reqparse.RequestParser()
        parser.add_argument('year', type=int, required=False, help='fetch all entries, or set a parameter: year=2019')
        args = parser.parse_args()
        year = args['year']
        return get_table_data('berlin_accidents', year), 200


# fetch all entries from table
def get_table_data(table_name, param):
    try:
        table_data = client[table_name]
        if param:
            payload = table_data[str(param)]
        else:
            payload = [data for data in table_data]
        return payload, 200
    except Exception as e:
        print('ERROR: Could not fetch table {}. Cause: {}'.format(table_name, e))
        return 'No data available. Try to change year parameter (year=2019) or leave it out to fetch all data.', 400



# fetch latest entry from table
def get_table_data_latest(table_name):
    try:
        table_data = client[table_name]   # not sure how only retreive the last document.
        payload = [data for data in table_data]
        if payload:
            return payload[0], 200 # this method is not optimal
        return 'No data available. Please validate your request and try again.', 400
    except Exception as e:
        print('ERROR: Could not fetch table >{}<. Cause: {}'.format(table_name, e))
        return e, 404


# disconnct from db on server shutdown
@atexit.register
def shutdown():
    try:
        client.disconnect()
        print('disconnected from db')
    except Exception:
        pass


if __name__ == '__main__':
    # run app
    app.run(debug=True)
