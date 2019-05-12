FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
COPY . /code/
WORKDIR /code/app/acts/
RUN pip install -r ../../requirements.txt
RUN pip install psycopg2
RUN pip install gunicorn
