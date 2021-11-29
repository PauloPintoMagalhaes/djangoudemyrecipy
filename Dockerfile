# Builds the image based on:
FROM python:3.7-alpine
MAINTAINER Paulo Magalhaes

# Prevents pythin buffering outputs, just prints them to prevent problems 
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# makes it so 
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# creates a user to run the process only
# limits the scope of attack if someone tries to get fresh wth our app
RUN adduser -D user
USER user
