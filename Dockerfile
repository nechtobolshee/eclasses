# pull official base image
FROM python:3.8.10
# set work directory
RUN mkdir /code
WORKDIR /code
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY ./entrypoint.sh .
RUN pip install -r requirements.txt
RUN chmod +x *.sh
# copy project
COPY . .
