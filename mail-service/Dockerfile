FROM python:3.8

RUN mkdir app

COPY . app/
WORKDIR app

RUN chmod +x requirements.txt

RUN pip install -r requirements.txt --no-cache-dir --compile

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=api
EXPOSE 5000

CMD flask run --host 0.0.0.0
