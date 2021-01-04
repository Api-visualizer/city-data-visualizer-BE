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
    return server.database("berlin_covid_intensivecare"), server.database("berlin_intensivecare_prediction")

def get_critical_status(db):
    dates, critical_status = [], []

    for item in db.all():
        critical = 0
        date = item["doc"]["date"]
        for feature in item["doc"]["features"]:
            status_ecmo = feature["properties"]["status"]["statusECMO"]
            status_highcare = feature["properties"]["status"]["statusHighCare"] 
            if status_ecmo != "KEINE_ANGABE" and status_highcare != "KEINE_ANGABE": 
                if status_ecmo != "VERFUEGBAR" or status_highcare != "VERFUEGBAR":
                    critical+=1
        dates.append(date)
        critical_status.append(critical)
    return dates, critical_status

def init_dataframe(dates, critical_status):
    df = pd.DataFrame(data={"dates": dates, "critical_status": critical_status})
    df["dates"] = pd.to_datetime(df["dates"], format="%d.%m.%Y")
    df = df.sort_values(by="dates")
    return df

def find_polynomial_regression(deg):
    coef = np.polyfit(np.arange(len(df["critical_status"].to_list())), df["critical_status"].to_list(), deg)
    return np.poly1d(coef)

def get_next_weeks_dates(df):
    dates_tail = df.tail(1)["dates"]
    ns = 1e-9 # Number of seconds in a nanosecond
    last_date = datetime.utcfromtimestamp(dates_tail.values[0].astype(int)*ns)
    return [(last_date+timedelta(days=x)).strftime("%d.%m.%Y") for x in range(1, 8)]     

def fill_data_object_with_prediction(df, p, data):
    pred_dates = df["dates"].dt.strftime("%d.%m.%Y").astype(str).to_list() # Convert dates
    pred_status= [round(p(x)) for x in np.arange(len(df["dates"].to_list()))]
    
    next_week = get_next_weeks_dates(df)
    pred_dates += next_week

    pred_indices = np.arange(len(pred_dates))[-7:]
    pred_status += [round(p(x)) for x in pred_indices]
    pred_status = [0 if i < 0 else i for i in pred_status] # Remove negative numbers

    data["prediction"]["x"] = pred_dates
    data["prediction"]["y"] = pred_status
    return {"date": pred_dates[-8], "data": data}

def post_data(db, data):
    if not any(document["doc"]["date"] == data["date"] for document in db.all()):   
        db.save(data)

if __name__ == "__main__":
    db, pred_db = init_databases()

    dates, critical_status = get_critical_status(db)
    data = {"prediction": {"x": [], "y": []}, "status": {"x": dates, "y": critical_status}}

    df = init_dataframe(dates, critical_status)

    deg = 6
    p = find_polynomial_regression(deg)    

    data = fill_data_object_with_prediction(df, p, data)
    post_data(pred_db, data)
