FROM python:3.9-alpine3.17

USER root

RUN apk update &&\
    apk upgrade &&\
    apk add build-base gcc python3-dev linux-headers

COPY requirements.txt .
COPY pickelmaster /pickelmaster
COPY pickelmaster_uwsgi.ini .

RUN mkdir vassals && ln -s /pickelmaster_uwsgi.ini /vassals

WORKDIR /pickelmaster

RUN pip install -U pip pip-tools setuptools wheel && pip-sync /requirements.txt && pip install uwsgi

CMD uwsgi --emperor /vassals