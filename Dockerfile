FROM python:3.7-alpine

# Install required packages and remove the apt packages cache when done.
#apk update && apk upgrade && \
RUN apk add --update build-base ca-certificates make g++ gcc libxslt-dev
RUN apk add \
    libjpeg \
    zlib \
    zlib-dev \
    libwebp \
    openjpeg \
    jpeg-dev \
    postgresql-libs \
    postgresql-dev \
    ncurses-dev \
    readline-dev \
    bash \
    libffi-dev \
    nginx \
    postgresql-client \
    supervisor

################################################################################
# устанавливаем парочку полезных утилит
RUN pip install ipython pgcli
RUN pip install uwsgi

# Install python 3.5 and pip3
#RUN apt-get install -y lib32ncurses5-dev build-essential libssl-dev libffi-dev python3
#RUN apt-get install -y python3-dev python3-pip libblas-dev libatlas-base-dev

RUN python -V
RUN python3 -V

ENV PYTHONUNBUFFERED 1

################################################################################
# создание служебных каталогов
# создание служебных каталогов
RUN mkdir -p /root/.ssh \
    /var/www/run \
    /var/www/app \
    /var/www/env \
    /var/www/media \
    /var/www/static \
    /var/www/log

################################################################################
# обрабатываемые ENTRYPOINT-ом пременные

ENV DB_BACKEND="" \
    DB_HOST="" \
    DB_PORT="" \
    DB_USER="" \
    DB_PASS="" \
    DB_NAME="" \
    CREATE_NEW_DB=0 \
    INIT_TEST_DATA=0 \
# 
    VIRTUAL_HOST="" \
# логин/пароль, которыми закрывается сайт
    HTTP_BASIC="" \
    HTTP_BASIC_USER="" \
    HTTP_BASIC_PASS=""

WORKDIR /var/www/app

################################################################################
# объявление аргументов, необходимых для доступа к репам
# если хоть одна из них изменится - все дальнейшие слои будут пересобраны
ARG HGRC
ARG SSH_PRIVATE_KEY
ARG SSH_CONFIG
ARG SSH_KNOWN_HOSTS

################################################################################
# установка зависимостей приложения

COPY /project/requirements /var/www/app/requirements
COPY /project/requirements.txt /var/www/app/requirements.txt
RUN pip install -r requirements.txt

COPY .add/supervisor-app.conf /etc/supervisor/conf.d/
COPY .add/uwsgi.ini /var/www/env/uwsgi.ini
COPY .add/uwsgi_params /var/www/env/uwsgi_params
COPY .add/nginx.conf /etc/nginx/
COPY .add/nginx-app.conf /etc/nginx/conf.d/
RUN rm /etc/nginx/conf.d/default.conf

COPY .add/docker-entrypoint.sh /docker-entrypoint.sh

COPY ./project /var/www/app

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisor-app.conf"]

EXPOSE 80
