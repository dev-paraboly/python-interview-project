FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7-2020-06-06

COPY requirements.txt .

RUN \
    apt-get update && \
    apt-get install python3-psycopg2 -y && \
    apt-get install gcc -y && \
    pip install -r requirements.txt --no-cache-dir

ENV TIMEOUT=600

COPY . /app