#FROM python:3.7.4-alpine3.10
FROM python:3.8-buster
#FROM python:3.7.4-slim-stretch
#FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get update  
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
WORKDIR /code/app/acts/
RUN pip install -r ../../requirements.txt
RUN pip install gunicorn
