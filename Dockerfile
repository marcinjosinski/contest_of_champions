FROM python:3.6-alpine

ENV FLASK_APP application.py

RUN mkdir -p /opt/contest_of_champions
WORKDIR /opt/contest_of_champions

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
