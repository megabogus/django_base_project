FROM python:3.7-alpine

RUN apk add --update build-base ca-certificates make g++ gcc libxslt-dev
RUN apk add \
    libjpeg \
    git \
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
    postgresql-client \
    libffi-dev


WORKDIR /app
COPY /project/requirements.txt /project/Makefile /app/
COPY /project/requirements /app/requirements/
RUN make req-dev

EXPOSE 8000