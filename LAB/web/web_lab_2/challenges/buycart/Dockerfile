FROM ubuntu:22.04

ARG admin

RUN apt-get update && apt-get install python3 python3-pip -y

COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install -r requirements.txt

COPY ./app /app


EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV FLASK_ENV=production

CMD flask run
