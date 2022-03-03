# pull official base image
#FROM python:3.6.12
FROM python:3.8.10

# set work directory
WORKDIR /src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# copy requirements file
COPY ./requirements.txt /src/requirements.txt
RUN apt update
RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install shapely


RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install -r /src/requirements.txt


# copy project
COPY . /src/