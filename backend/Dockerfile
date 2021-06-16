FROM python:3.7

ENV PYTHONUNBUFFERED 1

ARG DB_NAME=alphaorder
ARG DB_USERNAME=admin
ARG DB_PASSWORD=password
ARG DB_ENDPOINT=db
ARG DB_PORT=5432

ENV DB_NAME $DB_NAME
ENV DB_USERNAME $DB_USERNAME
ENV DB_PASSWORD $DB_PASSWORD
ENV DB_ENDPOINT $DB_ENDPOINT
ENV DB_PORT $DB_PORT

WORKDIR /backend
COPY . /backend

RUN pip install -r requirements.txt --no-cache-dir && \
    sed -i -e 's/{% load staticfiles %}/{% load static %}/' /usr/local/lib/python3.7/site-packages/rest_framework_swagger/templates/rest_framework_swagger/index.html && \
    apt update && \
    apt install -y cron

RUN chmod +x ./sleep.py

CMD python ./sleep.py && python manage.py runserver 0.0.0.0:8000