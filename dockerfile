#FROM python:3.7.4-alpine3.10
#FROM python:3.8-buster
#FROM python:3.7.4-slim-stretch
FROM python:3.12-alpine
ENV PYTHONUNBUFFERED 1
RUN apk update && apk add -u gcc musl-dev
#RUN apt-get install -y python3-dev python-dev default-libmysqlclient-dev
#RUN apt-get  install -y gcc
#RUN apk add --no-cache --virtual .build-deps\
#     build-base \
#     libxml2-dev \
#     libxslt-dev \
#     python-dev \
#     python3-lxml
#RUN apk del .fetch-deps \
RUN mkdir /code
COPY . /code/
WORKDIR /code/
RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install gunicorn
