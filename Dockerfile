# Builds the image based on:
FROM python:3.7-alpine
MAINTAINER Paulo Magalhaes

# Prevents python buffering outputs, just prints them to prevent problems 
ENV PYTHONUNBUFFERED 1

# installs requirements
COPY ./requirements.txt /requirements.txt
# apk is the alpine package manager
# --update updates the restry before adding the package
# --no-cache the registry index will not be stored in the docker container
RUN apk add --update --no-cache postgresql-client
# -- virtual sets up an alias for the dependencies pack so it can later be removed
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev
RUN pip install -r requirements.txt
# removes the packages under the alias .tmp-build.de
RUN apk del .tmp-build-deps

# makes app your docker working directory 
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# creates a user to run the process only
# limits the scope of attack if someone tries to get fresh wth our app
RUN adduser -D user
USER user
