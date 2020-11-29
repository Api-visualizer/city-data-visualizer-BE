from datetime import datetime
import urllib3
import os
from os.path import join, dirname
from dotenv import load_dotenv
import couchdb
import requests
urllib3.disable_warnings()
# Load .env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ADMIN = os.environ.get('ADMIN')
PASSWORD = os.environ.get('PASSWORD')
URL = os.environ.get('URL')
server_url = f"http://{ADMIN}:{PASSWORD}@{URL}/"
print(server_url)
couch = couchdb.Server(server_url)
db = couch['covid_age']

response = requests.get('https://www.berlin.de/lageso/gesundheit/infektionsepidemiologie-infektionsschutz/corona/tabelle-altersgruppen/index.php/index/all.json?q=')
data = response.json()['index']
new_date = datetime.now().strftime("%d.%m.%Y")

document = {'date': new_date, 'data': data}

data = [data for data in db]

if any(db[dat]['date'] == new_date for dat in data):
    print('already written')
else:
    print(f"write new date {new_date}")
    db.save(document)

'''
In der nachfolgenden Tabelle sind die an das LAGeSo übermittelten COVID-19 Infizierte (kumulativ) nach Altersgruppen aufgeführt.
Die Inzidenz (kumulativ) ist pro 100 000 Einwohner angegeben. Datenquelle Berliner Bevölkerung: 
Amt für Statistik Berlin-Brandenburg, Einwohnerregisterstatistik, Stichtag 31.12.2019 
'''