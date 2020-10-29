FROM python:latest

WORKDIR /usr/local/bin

COPY script.py .
COPY requirements.txt . 

RUN pip install -r requirements.txt

CMD ["python", "script.py"]
