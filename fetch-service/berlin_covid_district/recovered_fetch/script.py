import pandas as pd
from datetime import datetime, timedelta
import urllib3
import os
from os.path import join, dirname
from dotenv import load_dotenv
import pycouchdb

urllib3.disable_warnings()

# Load .env 
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def cleanup_dataframe(df):
    df["Meldedatum"] = pd.to_datetime(df["Meldedatum"], format="%Y-%m-%d")
    df["Landkreis"] = df["Landkreis"].str.replace("SK ", "")
    df = df[df["Bundesland"].str.contains("Berlin")]
    return df

def get_database(url):
    server = pycouchdb.Server(url)
    db = server.database("berlin_covid_district")
    return db

def recovered_by_district(df, district):
    by_district = df.loc[df["Landkreis"] == district]
    return int(by_district["SummeGenesen"]), int(by_district["AnzahlGenesen"])


df = pd.read_csv("https://opendata.arcgis.com/datasets/9644cad183f042e79fb6ad00eadc4ecf_0.csv")
df = cleanup_dataframe(df)

server_url = "http://{}:{}@couchdb.internal.datexis.com/".format(
        os.environ.get("COUCHDB_USERNAME"), 
        os.environ.get("COUCHDB_PASSWORD")
    )
db = get_database(server_url)

# Find latest date in dataset
dates = [item["doc"]["date"] for item in db.all()]
dates.sort(key=lambda date: datetime.strptime(date, "%d.%m.%Y"))
date_object = datetime.strptime(dates[-1], "%d.%m.%Y")
latest_date = date_object - timedelta(days=1) # recovered data is one day behind

df_date = latest_date.strftime("%Y-%m-%d") 
db_date = latest_date.strftime("%d.%m.%Y")

document = list(filter(lambda item: item["doc"]["date"] == db_date, list(db.all())))[0]
by_date = df.loc[df["Meldedatum"] == df_date]
      
# Set recovered values in district's feature properties
for district in by_date["Landkreis"].unique():
    feature = list(filter(lambda feature: feature["properties"]["GEN"] == district, document["doc"]["data"]["features"]))[0]
    
    total, new = recovered_by_district(by_date, district)
    feature["properties"]["total_recovered"] = total
    feature["properties"]["new_recovered"] = new         

db.save(document["doc"])
