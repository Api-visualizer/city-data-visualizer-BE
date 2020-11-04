# api-visualizer-BE

## how to start this backend-service
### on your machine

you need to export three environment variables before "flask run" 

EXPORT DB_USER=""

EXPORT DB_PW=""

EXPORT DB_URL=""

(on windows use SET instead of EXPORT)
```
cd database-service/
python3 -m venv venv
source venv/bin/activate
source .env
pip install -r requirements.txt
flask run 

```

### with docker
- requires a .env file in the database-service dir
- please make sure you're using the local.Dockerfile in the db-service directory!

```
cd database-service/
docker build -t cdv-backend:local . -f local.Dockerfile

docker run -p 5000:5000 cdv-backend:local
```

