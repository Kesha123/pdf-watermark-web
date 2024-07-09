FROM python:3.10

WORKDIR /app

COPY requirements.txt .
COPY script.py .

RUN pip install -r requirements.txt

CMD ["python", "script.py"]