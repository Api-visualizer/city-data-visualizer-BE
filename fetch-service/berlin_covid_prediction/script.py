
import os
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime, timedelta
import urllib3
import pycouchdb
import numpy as np
import pandas as pd


urllib3.disable_warnings()

# load .env 
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def init_databases():
    db_url = "http://{}:{}@141.64.3.248:5984".format(os.environ.get("COUCHDB_USERNAME"), os.environ.get("COUCHDB_PASSWORD"))
    server = pycouchdb.Server(db_url)
    return server.database("berlin_covid_sums"), server.database("berlin_covid_prediction")

def init_dataframe(dates, cases):
    df = pd.DataFrame(data={"dates": dates, "cases": cases})
    df["dates"] = pd.to_datetime(df["dates"], format="%d.%m.%Y")
    return df.sort_values(by="dates")

def find_polynomial_regression(deg):
    coef = np.polyfit(np.arange(len(dates)), cases, deg)
    p = np.poly1d(coef)
    return p

def get_next_weeks_dates():    
    dates_tail = df.tail(1)["dates"]
    ns = 1e-9 # Number of seconds in a nanosecond
    last_date = datetime.utcfromtimestamp(dates_tail.values[0].astype(int)*ns)
    return [(last_date+timedelta(days=x)).strftime("%d.%m.%Y") for x in range(1, 8)]

def fill_data_object(dates, cases, p):
    data = {"regression": {"x": [], "y": []}, "cases": {"x": dates, "y": cases}}

    next_week = get_next_weeks_dates()
    data["date"] = next_week[0]

    pred_dates = dates    
    pred_dates += next_week
    pred_cases = [round(p(x),2) for x in np.arange(len(dates))]
    pred_cases += [round(p(x),2) for x in np.arange(len(pred_dates))[-7:]]

    data["regression"]["x"] = pred_dates
    data["regression"]["y"] = pred_cases    
    return data

def post_data(db, data):
    if not any(document["doc"]["date"] == data["date"] for document in db.all()):    
        db.save(data)

if __name__ == "__main__":    
    db, pred_db = init_databases()

    dates = [document["doc"]["date"] for document in db.all()] 
    cases = [document["doc"]["cases"] for document in db.all()]
    df = init_dataframe(dates, cases)

    deg = 9
    p = find_polynomial_regression(deg) # TODO: Find degree that fits the best or store multiple regressions
 
    dates = df["dates"].dt.strftime("%d.%m.%Y").astype(str).to_list() # Convert dates
    data = fill_data_object(dates, cases, p)

    post_data(pred_db, data)
