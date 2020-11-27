FROM python:latest

COPY main.py .
COPY .env .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]