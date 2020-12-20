import urllib3
import couchdb
from datetime import datetime
urllib3.disable_warnings()
import os

ADMIN = os.environ.get('DB_USER')
PASSWORD = os.environ.get('DB_PW')
URL = os.environ.get('DB_URL')

server_url = f"http://{ADMIN}:{PASSWORD}@{URL}/"
couch = couchdb.Server(server_url)

db = couch['berlin_covid_district']
legend_db = couch['covid_map_legend']

list = []
for id in db:
    docs = db[id]
    data = docs['data']['features']

    for district in data:
        list.append(district['properties']['cases_per_100k'])

min = int(min(list))
max = int(max(list))

stepsize = int(max/10)

print(f'{min} {max}')
print(f'\nstepsize: {stepsize}')

steps = []
new_step = 0
for i in range(0, 10):
    new_step += stepsize
    steps.append(int(new_step))

colors = ['#b0091f', '#ff0000', '#e63030', '#ff4800', '#e3661e', '#fc7e2a', '#ffc72e', '#f0de56', '#fff67d', '#9eff4a']
data = [{steps[i]: colors[i]} for i in range(0, 10)]

_id = datetime.now().strftime("%d.%m.%Y")
if legend_db.info()['doc_count'] != 0:
    for legend_id in legend_db:
        doc = legend_db[legend_id]
        legend_db.delete(doc)
    legend_db.save({'_id': _id, 'legend': data})

