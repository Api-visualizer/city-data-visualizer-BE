FROM python:latest

WORKDIR /app

COPY preprocess_data_covidmap.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python3", "preprocess_data_covidmap.py"]
