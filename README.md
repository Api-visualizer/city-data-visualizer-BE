# api-visualizer-BE

- vpn required

## how to start this backend-service
### on your machine

you need to export three environment variables before "flask run" 

export DB_USER=""

export DB_PW=""

export DB_URL=""

(on windows use set instead of export)
```
cd database-service/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DB_USER=
export DB_PW=
export DB_URL=
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

## docker container clean up
docker ps shows you all running container on your machine. 

```
docker stop $(docker ps -a -q)
```

