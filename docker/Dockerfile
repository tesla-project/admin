FROM python:3-alpine3.7

MAINTAINER Xavier Baro <xbaro@uoc.edu>

ENV SECRET_PREFIX ADMIN
ENV INSTRUMENT_PORT 443
ENV FLASK_APP manage.py

RUN apk add --update --no-cache unzip wget cmake alpine-sdk\
      nginx bash git gcc g++ make openrc gettext postgresql-dev libffi-dev python-dev linux-headers netcat-openbsd

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install uWSGI

COPY docker/cert/SERVER_CERT /run/secrets/${SECRET_PREFIX}SERVER_CERT
COPY docker/cert/SERVER_KEY /run/secrets/${SECRET_PREFIX}SERVER_KEY
COPY docker/cert/SERVER_CA /run/secrets/${SECRET_PREFIX}SERVER_CA
COPY docker/cert/CLIENT_CERT /run/secrets/${SECRET_PREFIX}CLIENT_CERT
COPY docker/cert/CLIENT_KEY /run/secrets/${SECRET_PREFIX}CLIENT_KEY
COPY docker/cert/CLIENT_CA /run/secrets/${SECRET_PREFIX}CLIENT_CA

# Copy configuration files
COPY docker/conf/emperor /etc/uwsgi
COPY docker/conf/nginx.vh.default.conf /app/
COPY docker/conf/nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /var/log/service_uwsgi /logs

# setup application
WORKDIR /app
COPY manage.py .

# Add migrations folder
COPY migrations migrations

# Copy the start script
COPY bin/run_service.py .

# Create running folder for Nginx
RUN mkdir /run/nginx

# Prepare starting script
COPY bin/start_service.sh .
RUN chmod +x start_service.sh

# Copy the instrument code
COPY tesla_admin tesla_admin

# Copy the models
COPY tesla_models tesla_models

ENTRYPOINT ["/bin/bash"]
CMD ["/app/start_service.sh"]

RUN mkdir -p /app/data
COPY data_admin /app/data_admin