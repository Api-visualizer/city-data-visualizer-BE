from flask import Flask
from flask_cors import CORS
from flask_restplus import reqparse

from db import get_table_data, get_table_data_by_id, get_latest_table_data
from datetime import datetime


app = Flask(__name__)
CORS(app)


# Routes
@app.route('/api/v1/berlin-shapes-district')
def get_berlin_shapes():    
    return get_table_data('berlin_shapes_district')


@app.route('/api/v1/berlin-covid-age')
def get_covid_per_age():
    return get_table_data('covid_age')


@app.route('/api/v1/berlin-covid-district')
def get_covid_per_district():
    return get_table_data('berlin_covid_district')


@app.route('/api/v1/berlin-covid-district/latest')
def get_covid_per_district_latest():
    time_format = '%d.%m.%Y'
    dates = lambda x: datetime.strptime(x['doc']['date'], time_format)
    return get_latest_table_data('berlin_covid_district', dates)


@app.route('/api/v1/berlin-covid-intensive-care')
def get_covid_intensive_care():
    return get_table_data('berlin_covid_intensivecare')


@app.route('/api/v1/berlin-covid-intensive-care/latest')
def get_covid_intensive_care_latest():
    time_format = '%d.%m.%Y'
    dates = lambda x: datetime.strptime(x['doc']['date'], time_format)
    return get_latest_table_data('berlin_covid_district', dates)


@app.route('/api/v1/berlin-accidents')
def get_accidents(): 
    # Define parser and request args
    parser = reqparse.RequestParser()
    parser.add_argument('year', type=int, required=False, help='You can set a parameter: year=2019')
    parser.add_argument('type', type=str, required=False, help="You can set a parameter: type='foot' | options are: bike, car, foot, motorcycle, truck")
    parser.add_argument('hour', type=str, required=False, help="You can set a parameter: hour='16' | values form 0-24")
    args = parser.parse_args()
    
    year, accident_type, hour = args['year'], args['type'], args['hour']
    if year:
        return get_accident_data('berlin_accidents', year=year, type=accident_type, hour=hour)
    return get_table_data('berlin_accidents')


@app.route('/api/v1/berlin-cancer')
def get_cancer_diagnoses():
    return get_cancer_diagnoses_data('berlin_cancer')


# Helper methods
def get_accident_data(table_name, **kwargs):
    year, accident_type, hour = kwargs['year'], kwargs['type'], kwargs['hour']

    payload = get_table_data_by_id(table_name, 'geojson_{}'.format(str(year)))
    if payload[1] == 200:         
        data = payload[0]['data']        
        if accident_type:
            filter_list = list(filter(lambda x: x['properties']['type'][accident_type] > 0, data['accidents']['features']))
            data['accidents']['features'] = filter_list
        if hour:
            filter_list = list(filter(lambda x: x['properties']['meta']['USTUNDE'] == int(hour), data['accidents']['features']))
            data['accidents']['features'] = filter_list
        return {'data': data}, 200
    return payload

def get_cancer_diagnoses_data(table_name):    
    response = get_table_data('berlin_cancer')

    if response[1] == 200:
        cleaned_data = {}
        payload = response[0]['data'] 

        for data in payload:
            year = list(data['doc'].keys())[2]        
            del data['doc']['_id']
            del data['doc']['_rev']
            cleaned_data[year] = data['doc'][year]
        
        for year in list(cleaned_data.keys()):
            clean_data = cleaned_data[year]
            for clean_dat in clean_data:
                clean_dat['age'] = clean_dat['age'].strip()
                clean_dat['age'] = clean_dat['age'].replace("  ", " ").replace("  ", " ")
        return {'data': cleaned_data}, 200
    return response


# Run app
if __name__ == '__main__':
    app.run(debug=True)
