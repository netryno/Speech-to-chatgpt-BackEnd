# pull official base image
#FROM python:3.6.12
FROM python:3.8.10

# set work directory
WORKDIR /src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y flac

RUN apt-get install -y ffmpeg
RUN apt-get install -y libespeak-dev
# copy requirements file
COPY ./requirements.txt /src/requirements.txt
RUN apt update
RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install -r /src/requirements.txt
#RUN python3 -m pip install whisper --upgrade
RUN python3 -m pip install -U openai-whisper
# copy project
COPY . /src/