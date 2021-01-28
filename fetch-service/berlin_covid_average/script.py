import os
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime
import urllib3
import pycouchdb
import urllib3
import numpy as np
import pandas as pd
import bottleneck as bn


urllib3.disable_warnings()

# load .env 
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def init_databases():
    db_url = "http://{}:{}@141.64.3.248:5984".format(os.environ.get("COUCHDB_USERNAME"), os.environ.get("COUCHDB_PASSWORD"))
    server = pycouchdb.Server(db_url)
    return server.database("berlin_covid_sums"), server.database("berlin_covid_moving_average")

def init_dataframe(dates, cases):
    df = pd.DataFrame(data={"dates": dates, "cases": cases})
    df["dates"] = pd.to_datetime(df["dates"], format="%d.%m.%Y")
    return df.sort_values(by="dates")

def post_data(db, data): 
    if not any(document["doc"]["date"] == data["date"] for document in db.all()):    
        db.save(data)

if __name__== "__main__":
    sums_db, mm_db = init_databases()
    dates = [document["doc"]["date"] for document in sums_db.all()] 
    cases = [document["doc"]["cases"] for document in sums_db.all()]
    df = init_dataframe(dates, cases)   

    mm = bn.move_mean(df["cases"].to_list(), window=7, min_count=1)

    today = datetime.today()
    date = datetime.strftime(today, "%d.%m.%Y")
    data = {"date": date, 
        "data": {
            "moving_average": list(mm), 
            "dates": list(df["dates"].dt.strftime('%d.%m.%Y')), 
            "cases": list(df["cases"])
            } 
       }

    post_data(mm_db, data)