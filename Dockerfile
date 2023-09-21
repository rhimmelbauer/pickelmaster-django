FROM python:3.9-alpine3.17

USER root

RUN apk update &&\
    apk upgrade &&\
    apk add build-base gcc musl-dev python3-dev 

COPY requirements.txt .
COPY pickelmaster /pickelmaster

WORKDIR /pickelmaster

RUN pip install -U pip pip-tools && pip-sync /requirements.txt

CMD python manage.py runserver 0.0.0.0:8000