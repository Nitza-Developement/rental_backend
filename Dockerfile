# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN yes yes | apt-get install python-psycopg2
RUN apt-get install -y python3-cffi   
RUN apt-get install -y python3-brotli
RUN apt-get install -y libpango-1.0-0
RUN apt-get install -y libpangoft2-1.0-0

RUN apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
RUN pip install gunicorn
COPY ./requirements.txt .
RUN pip install -r requirements.txt


# copy project
COPY . .





