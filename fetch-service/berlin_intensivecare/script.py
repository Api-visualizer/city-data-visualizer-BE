import requests
import datetime
from geojson import Feature, Point, FeatureCollection
import pycouchdb
import os
from os.path import join, dirname
from dotenv import load_dotenv
import urllib3

urllib3.disable_warnings()

# Load .env 
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def get_database(url):
    server = pycouchdb.Server(url)
    db = server.database("berlin_covid_intensivecare")
    return db

server_url = "http://{}:{}@couchdb.internal.datexis.com/".format(
        os.environ.get("COUCHDB_USERNAME"), 
        os.environ.get("COUCHDB_PASSWORD")
    )
db = get_database(server_url)

response = requests.get("https://www.intensivregister.de/api/public/intensivregister?bundesland=BERLIN")
data = response.json()

date = datetime.datetime.now().strftime("%d.%m.%Y")
document = list(filter(lambda item: item["doc"]["date"] == date, list(db.all())))

if len(document) == 0:    
    feature_list = []
    for feature in data["data"]:    
        feature_list.append(Feature(
            geometry=Point((
                feature["krankenhausStandort"]["position"]["longitude"], 
                feature["krankenhausStandort"]["position"]["latitude"])),
            properties={
                "name": feature["krankenhausStandort"]["bezeichnung"],
                "status": feature["bettenStatus"],
                "last_update": feature["meldezeitpunkt"],
            }
        ))
        
    feature_collection = FeatureCollection(feature_list)
    feature_collection["date"] = date
    db.save(feature_collection)
