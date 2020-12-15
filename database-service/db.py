import pycouchdb
import urllib3
import os, sys


urllib3.disable_warnings() # Disable missing certificate warnings

# Connect to db
def init_db():
    USER, PASS, URL = os.environ.get('DB_USER'), os.environ.get('DB_PW'), os.environ.get('DB_URL')
    return pycouchdb.Server('http://{}:{}@{}'.format(USER, PASS, URL))

server = init_db()

# Database access
def get_table_data(table_name):
    try:
        table_data = server.database(table_name).all()     
        return {'data': list(table_data)}, 200
    except Exception as e:
        print('ERROR: Could not fetch table {}. Cause: {}'.format(table_name, e))
        return {'error': 'No data available. Try other parameter values.'}, 400

def get_latest_table_data(table_name, dates):
    try:
        table_data = server.database(table_name).all()
        table_document = sorted(list(table_data), key=dates)[-1]        
        return {'data': table_document}, 200
    except Exception as e:
        print('ERROR: Could not fetch table {}. Cause: {}'.format(table_name, e))
        return {'error': 'No data available. Try other parameter values.'}, 400

def get_table_data_by_id(table_name, id):
    try:
        table_document = server.database(table_name).get(id) 
        return {'data': table_document}, 200
    except Exception as e:
        print('ERROR: Could not fetch table {}. Cause: {}'.format(table_name, e))
        return {'error': 'No data available. Try other parameter values.'}, 400
