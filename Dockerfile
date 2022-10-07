# syntax=docker/dockerfile:1

FROM python:3.8 AS builder

COPY . .
RUN pip3 install -r requirements.txt
#FROM python:3.8-slim
WORKDIR /app
ADD . /app/

CMD [ "python", "-u" , "./send.py"]