# api-visualizer-BE

## starting database-service
```
cd database-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run 

```

### with docker
```
docker build db-service:local

docker run -p 5000:5000 db-service:local
```