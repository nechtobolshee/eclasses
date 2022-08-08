FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y\
    && apt-get install software-properties-common -y\
    && add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main"\
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -\
    && apt-get update\
    && apt-get install -y git gcc libspatialindex-dev python3-dev cmake curl libcurl4-openssl-dev python3-setuptools \
    postgresql-client-13

RUN apt-get install -y cron

RUN mkdir /code
WORKDIR /code

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
