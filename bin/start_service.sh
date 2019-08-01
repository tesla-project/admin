#!/usr/bin/env bash

if [ "$USE_GIT_CONFIG" -eq 0 ]; then
    echo "Waiting for database connection..."
    until nc -z -v -w30 $DB_HOST $DB_PORT
    do
      sleep 1
    done
else
    cp /app/data/certs/modules/admin.${DOMAIN}/cert.pem /run/secrets/${SECRET_PREFIX}SERVER_CERT
    cp /app/data/certs/modules/admin.${DOMAIN}/key.pem /run/secrets/${SECRET_PREFIX}SERVER_KEY
    cp /app/data/certs/deploy-manager/ca.pem /run/secrets/${SECRET_PREFIX}SERVER_CA
fi

# Perform migrations
flask db upgrade

# Start uwsgi
uwsgi --emperor /etc/uwsgi/emperor.ini &

# Initialize Nginx configuration
envsubst '${INSTRUMENT_PORT}:${SECRET_PREFIX}' < /app/nginx.vh.default.conf > /etc/nginx/conf.d/default.conf

# Start Nginx
nginx