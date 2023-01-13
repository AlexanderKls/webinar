FROM ubuntu:20.04

MAINTAINER Alexander Kolesnik "alexanderpsk60@gmail.com"

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get -yq install net-tools nginx python3-pip mysql-client

RUN pip install uwsgi flask supervisor

RUN useradd -ms /bin/bash aurora && \
    rm -f /etc/nginx/fastcgi.conf /etc/nginx/fastcgi_params && \
    rm -f /etc/nginx/snippets/fastcgi-php.conf /etc/nginx/snippets/snakeoil.conf

EXPOSE 80

COPY /opt/mydocker/supervisord.conf /etc/supervisord.conf
COPY /opt/mydocker/wsgi.ini /etc/uwsgi/wsgi.ini

ENTRYPOINT ["/usr/local/bin/supervisord"]
