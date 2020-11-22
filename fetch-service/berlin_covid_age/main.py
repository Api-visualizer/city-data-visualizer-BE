import pandas as pd
from datetime import datetime, timedelta
import urllib3
import os
import simplejson as j
from os.path import join, dirname
from dotenv import load_dotenv
import couchdb
import requests
import csv
urllib3.disable_warnings()
# Load .env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

os.environ.get('ADMIN')
os.environ.get('PASSWORD')
os.environ.get('URL')
server_url = f"https://{ADMIN}:{PASSWORD}@{URL}"
couch = couchdb.Server(server_url)

response = requests.get('https://www.berlin.de/lageso/gesundheit/infektionsepidemiologie-infektionsschutz/corona/tabelle-altersgruppen/index.php/index/all.json?q=')
data = response.json()['index']
dataset = couch['covid_age']
date = datetime.now().strftime("%d.%m.%Y")
document = {'date': date, 'data': data}
dataset.save(document)


