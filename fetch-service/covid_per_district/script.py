import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests
import pycouchdb
import urllib3
import json

urllib3.disable_warnings()

# load .env 
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# get data
res = requests.get("https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=1%3D1&outFields=death_rate,cases,deaths,last_update,recovered,GEN,cases_per_100k,cases_per_population&outSR=4326&f=geojson")
data = res.json()

# cleanup data
features = []

for i, feature in enumerate(data["features"]):
    if "Berlin" in data["features"][i]["properties"]["GEN"]:
        del feature["geometry"]
        features.append(feature)

data["features"] = features
del data["crs"]

# store data
obj = {
    "date": data["features"][0]["properties"]["last_update"][:10],
    "data": data
}

server_url = "http://{}:{}@couchdb.internal.datexis.com/".format(os.environ.get("COUCHDB_USERNAME"), os.environ.get("COUCHDB_PASSWORD"))
server = pycouchdb.Server(server_url)
db = server.database("covid_per_district")

if not any(document["doc"]["date"] == obj["date"] for document in db.all()):
    db.save(obj)
