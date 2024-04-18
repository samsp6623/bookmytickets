FROM python:3.11.4-slim-buster
WORKDIR /usr/src/app

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt