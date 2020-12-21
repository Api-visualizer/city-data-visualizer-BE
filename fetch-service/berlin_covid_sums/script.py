import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests
import json
from datetime import datetime, timedelta
import urllib3
import pycouchdb

urllib3.disable_warnings()

# load .env 
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

db_url = "http://{}:{}@141.64.3.248:5984".format(os.environ.get("COUCHDB_USERNAME"), os.environ.get("COUCHDB_PASSWORD"))
server = pycouchdb.Server(db_url)
db = server.database("berlin_covid_sums")

def add_leading_zero(string):
    if len(string) < 2:
        return "0" + string
    return string

yesterday = datetime.today()-timedelta(days=1)
d, m, y = add_leading_zero(str(yesterday.day)), add_leading_zero(str(yesterday.month)), yesterday.year
date = "{}.{}.{}".format(d, m, y)

base_url = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Covid19_RKI_Sums/FeatureServer/0/query?where=IdBundesland%3D11+AND+Meldedatum+%3D+TIMESTAMP+%27{}+00%3A00%3A00%27&objectIds=&time=&resultType=standard&outFields=&returnIdsOnly=true&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=standard&f=pjson&token="
feature_url = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0/{}?f=pjson"

def find_documents_by_ids(ids):
    documents = []
    for i in ids:
        url = feature_url.format(i)
        feature = json.loads(requests.get(url).text)
        documents.append(feature)
    return documents

def sum_cases_and_deaths(documents):
    cases, deaths = 0, 0
    for document in documents:
        cases += document["feature"]["attributes"]["AnzahlFall"]
        deaths += document["feature"]["attributes"]["AnzahlTodesfall"]
        time.sleep(random.uniform(0,1))
    return cases, deaths

def post_to_db(month, day, cases, deaths):
    date = "{}.{}.2020".format(day, month)    
    return db.save({"date": date, "cases": cases, "deaths": deaths})

if not any(document["doc"]["date"] == date for document in db.all()): 
    timestamp = "{}-{}-{}".format(y, m, d)
    url = base_url.format(timestamp)
    data = json.loads(requests.get(url).text)
    
    documents = find_documents_by_ids(data["objectIds"])
    cases, deaths = sum_cases_and_deaths(documents)
        
    post_to_db(m, d, cases, deaths)
