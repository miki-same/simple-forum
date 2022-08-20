FROM python:3.8-slim

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
RUN apt-get install build-essential python -y
RUN apt-get install nginx -y

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

WORKDIR /app
COPY . /app

RUN cp nginx/uwsgi.conf /etc/nginx/conf.d/
RUN rm ../etc/nginx/sites-enabled/default
RUN mkdir ../var/log/uwsgi

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

