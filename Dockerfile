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
RUN apk add --update --no-cache postgresql-client jpeg-dev
# -- virtual sets up an alias for the dependencies pack so it can later be removed
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev musl-dev \
        zlib zlib-dev
RUN pip install -r /requirements.txt
# removes the packages under the alias .tmp-build.de
RUN apk del .tmp-build-deps

# makes app your docker working directory 
RUN mkdir /app
WORKDIR /app
COPY ./app/ /app

# media that might be uplload
RUN mkdir -p /vol/web/media
# media that will not be changed and is used by our app
RUN mkdir -p /vol/web/static
# creates a user to run the process only
# limits the scope of attack if someone tries to get fresh wth our app
RUN adduser -D user
# sets all volumes within /vol/ to user
RUN chown -R user:user /vol/
# sets so user can change at will, but other can only read
RUN chmod -R 755 /vol/web
USER user
