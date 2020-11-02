from cloudant import Cloudant
from flask import Flask
from flask_restful import Resource, Api
from flasgger import Swagger, swag_from
import atexit

import os

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'City Data Visualizer',
    'uiversion': 3
}
swagger = Swagger(app)
api = Api(app)
client = None


class CovidPerDistrict(Resource):
    @swag_from('api.yml', validation=False)
    def get(self):
        table_data = client['covid_per_district']
        payload = [data for data in table_data]
        return payload, 200


@atexit.register
def shutdown():
    client.disconnect()
    print('disconnected from db')


api.add_resource(CovidPerDistrict, '/api/v1/covid')


if __name__ == '__main__':
    # connect to db
    client = Cloudant(os.environ.get('DB_USER'), os.environ.get('DB_PW'),
                      url=os.environ.get('DB_URL'),
                      connect=True,
                      auto_renew=True)
    # run app
    app.run(debug=True)