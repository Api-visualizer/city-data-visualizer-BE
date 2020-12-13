from flask import Flask
from flask_restful import reqparse

import os, sys
import pycouchdb
import urllib3


urllib3.disable_warnings() # Disable missing certificate warning

app = Flask(__name__)


# Connect to db
USER = os.environ.get('DB_USER')
PASS = os.environ.get('DB_PW')
URL = os.environ.get('DB_URL')
server = pycouchdb.Server("http://{}:{}@{}".format(USER, PASS, URL))



# Routes
@app.route("/api/v1/berlin-covid-age")
def get_covid_per_age():
    return get_table_data("covid_age"), 200


@app.route("/api/v1/berlin-shapes-district")
def get_district_shapes():
    return get_table_data("berlin_shapes_district"), 200


@app.route("/api/v1/berlin-covid-district")
def get_covid_per_district():
    return get_table_data("berlin_covid_district"), 200


@app.route("/api/v1/berlin-covid-district/latest")
def get_covid_per_district_latest():
    return get_latest_table_data("berlin_covid_district"), 200


@app.route("/api/v1/berlin-accidents")
def get_accidents():
    parser = reqparse.RequestParser()
    parser.add_argument("year", type=int, required=True, help="You can set a parameter: year=2019")
    parser.add_argument("type", type=str, required=False, help="You can set a parameter: type='pedestrian' | Options are: bike, car, motorcycle, truck, pedestrian, other")
    parser.add_argument("hour", type=str, required=False, help="You can set a parameter: hour='16' | Values form 0-24")
    
    args = parser.parse_args()    
    year, accident_type, hour = args["year"], args["type"], args["hour"]
    return get_accident_data("berlin_accidents", year=year, type=accident_type, hour=hour)



# Helper methods
def get_accident_data(table_name, **kwargs):
    year, accident_type, hour = kwargs["year"], kwargs["type"], kwargs["hour"]
    
    try:        
        payload = get_document_by_id(table_name, "geojson_{}".format(year))

        if accident_type:
            filter_list = list(filter(lambda x: x["properties"]["type"][accident_type] > 0, payload["accidents"]["features"]))
            payload["accidents"]["features"] = filter_list
        if hour:
            filter_list = list(filter(lambda x: x["properties"]["meta"]["USTUNDE"] == int(hour), payload["accidents"]["features"]))
            payload["accidents"]["features"] = filter_list
        return dict(payload), 200
    except Exception as e:
        print("ERROR: Could not fetch table {}. Cause: {}".format(table_name, e))
        return "No data available. Try other parameter values.", 400


# Database access
def get_table_data(table_name):    
    return {"data": list(server.database(table_name).all())}

def get_latest_table_data(table_name):
    return list(server.database(table_name).all())[-1]

def get_document_by_id(table_name, id):
    return server.database(table_name).get(id)