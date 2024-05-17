FROM python:3.12-slim-bullseye

WORKDIR /app

COPY req.txt /app
COPY .env /app

RUN pip install -r req.txt