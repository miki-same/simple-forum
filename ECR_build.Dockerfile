#Dockerイメージ作成用のDockerfile

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

ENV SIMPLE_FORUM_CONFIG production
ENV SIMPLE_FORUM_SECRET_KEY 4eb223395f8025edc0838eba8242e08dab92ea19ed7deea6
ENV SIMPLE_FORUM_AWS_ACCESS_KEY  AKIASHWOWBPOZ634P2GE
ENV SIMPLE_FORUM_AWS_SECRET_ACCESS_KEY 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

WORKDIR /app
COPY . /app

RUN cp nginx/uwsgi.conf /etc/nginx/conf.d/
RUN rm ../etc/nginx/sites-enabled/default
RUN mkdir ../var/log/uwsgi

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

CMD ["sh","run.sh"]