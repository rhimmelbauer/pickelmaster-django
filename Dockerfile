FROM python:3.9-alpine3.17

USER root

RUN apk update &&\
    apk upgrade &&\
    apk add build-base gcc python3-dev linux-headers nginx

COPY requirements.txt .
COPY pickelmaster /pickelmaster
COPY nginx.conf /etc/nginx/sites-available/pickelmaster.conf

RUN ln -s /etc/nginx/sites-available/pickelmaster.conf /etc/nginx/sites-enabled/

WORKDIR /pickelmaster

RUN pip install -U pip pip-tools setuptools wheel && pip-sync /requirements.txt && pip install uwsgi

CMD uwsgi --socket pickelmaster.sock --module pickelmaster.wsgi