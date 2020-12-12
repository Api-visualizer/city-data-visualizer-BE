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

ADMIN = os.environ.get('ADMIN')
PASSWORD = os.environ.get('PASSWORD')
URL = os.environ.get('URL')

server_url = f"http://{ADMIN}:{PASSWORD}@{URL}/"
new_server_url = 'http://admin:couchdbpassword123@141.64.3.244:5984/'

couch = couchdb.Server(server_url)
new_couch = couchdb.Server(new_server_url)

db_names = ['berlin_cancer','berlin_accidents', 'berlin_covid_district', 'berlin_covid_intensivecare',
            'berlin_cycling_routes', 'berlin_shapes_district', 'covid_age']

for database in db_names:
    try:
        db = couch[database]
        new_couch.create(database)
        new_db = new_couch[database]
        ids = [data for data in db]
        for id in ids:
            data = db[id]
            filename = f'{db}-{id}.json'
            data = json.loads(json.dumps(data))
            del data['_id']
            del data['_rev']
            new_db.save(data)
            print(f'saved {id} in {database} ')
    except Exception:
        print(f'something went wrong {database}')







