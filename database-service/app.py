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
# connect to db
client = Cloudant(os.environ.get('DB_USER'), os.environ.get('DB_PW'),
                  url=os.environ.get('DB_URL'),
                  connect=True,
                  auto_renew=True)

swagger = Swagger(app)
api = Api(app)

# run app
app.run(debug=True)

# classes
class BerlinVerschenken(Resource):
    @swag_from('api.yml', validation=False)
    def get(self):
        return get_table_data('berlin_verschenken'), 200


class BerlinCovidDistrict(Resource):
    @swag_from('api.yml', validation=False)
    def get(self):
        return get_table_data('berlin_covid_district'), 200


class Json(Resource):
    @swag_from('api.yml', validation=False)
    def get(self):
        return {'json sagt': 'hallo i bims, der json'}, 200

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


# register endpoints
api.add_resource(BerlinVerschenken, '/api/v1/berlin-verschenken')
api.add_resource(BerlinCovidDistrict, '/api/v1/berlin-covid-district')
api.add_resource(Json, '/')
