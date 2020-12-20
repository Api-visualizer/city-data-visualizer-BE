import urllib3
import os
from os.path import join, dirname
from dotenv import load_dotenv
import couchdb
import json

urllib3.disable_warnings()

# Load .env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ADMIN = 'admin'
PASSWORD = 'password'
URL = '141.64.3.248:5984'

server_url = f"http://{ADMIN}:{PASSWORD}@{URL}/"
print(server_url)
couch = couchdb.Server(server_url)

database = 'berlin_accidents'

db = couch[database]
new_db = couch.create('berlin_accidents_preprocessed')

for id in db:
    data = db[id]
    if id == 'geojson_2018' or id == 'geojson_2019':
        try:
            accidents = data['accidents']['features']
            for acc in accidents:
                acc['geometry']['coordinates'][0] = acc['geometry']['coordinates'][0].replace(',', '.')
                acc['geometry']['coordinates'][1] = acc['geometry']['coordinates'][1].replace(',', '.')
            data['_id'] = id
            del data['_rev']
            new_db.save(data)
            print(data.keys())
        except Exception as e:
            print(e)
    else:
        accidents = data['accidents']
        try:
            for key in accidents.keys():
                accidents[key]['lat'] = accidents[key]['lat'].replace(',', '.')
                accidents[key]['long'] = accidents[key]['long'].replace(',', '.')
            data['_id'] = id
            del data['_rev']
            new_db.save(data)
            print(data.keys())
        except Exception as e:
            print(e)
