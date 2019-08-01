#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  TeSLA Admin
#  Copyright (C) 2019 Universitat Oberta de Catalunya
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from logging.handlers import RotatingFileHandler
import logging
import sys

PG_URL = 'postgresql://{}:{}@{}:{}/{}'
RABBITMQ_URL = 'amqp://{}:{}@{}/{}'
result_backend_format = 'db+postgresql://{}:{}@{}:{}/{}'


def get_secret(secret_name, default=None):
    secret_prefix = os.environ.get('SECRET_PREFIX', 'TESLA_ADMIN')
    secret_filename = os.path.join('/run/secret/', '{}{}'.format(secret_prefix, secret_name))

    if os.path.isfile(secret_filename):
        with open(secret_filename, 'r') as content_file:
            content = content_file.read()
            return content
    else:
        return os.getenv(secret_name, default)


def get_configuration_value(key, default=None):
    if bool(int(os.getenv('USE_GIT_CONFIG', False))):
        from .git_config import get_config_value
        value = get_config_value(key)
        if value is not None:
            return value

    # Try to read this value from secrets or environment variable
    return get_secret(key, default)


class BaseConfig(object):
    DEBUG = get_configuration_value('DEBUG', False)
    SECRET_KEY = get_configuration_value('SECRET_KEY', 'bf0926d3-1fd6-4d26-bb79-fb845c')
    SECRET_PREFIX = get_configuration_value('SECRET_PREFIX', 'TESLA_ADMIN')
    
    # Module description
    MODULE_NAME = get_configuration_value('MODULE_NAME', 'ADMIN')
    MODULE_VERSION = get_configuration_value('MODULE_VERSION', 'N/A')
    CONFIG_NAME = get_configuration_value('CONFIG', 'production')

    # Allow to use local libraries or remote ones on templates
    USE_LOCAL_LIBS = bool(int(get_configuration_value('USE_LOCAL_LIBS', 0)))

    # Certificate configurations
    DOMAIN = get_configuration_value('DOMAIN', None)
    COUNTRY = get_configuration_value('COUNTRY', None)
    INSTITUTION = get_configuration_value('INSTITUTION', None)


class DBConfig(BaseConfig):
    # Get Database configuration
    DB_USER = get_configuration_value('DB_USER', None)
    DB_HOST = get_configuration_value('DB_HOST', 'localhost')
    DB_PORT = int(get_configuration_value('DB_PORT', 5432))
    DB_NAME = get_configuration_value('DB_NAME', 'tesla')
    DB_PASSWORD = get_configuration_value('DB_PASSWORD', None)

    # Setup SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = PG_URL.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)


class RabbitConfig(BaseConfig):
    # Get RabbitMQ parameters
    RABBITMQ_USER = get_configuration_value('RABBITMQ_USER', 'rabbitmq')
    RABBITMQ_HOST = get_configuration_value('RABBITMQ_HOST', 'localhost')
    RABBITMQ_PORT = int(get_configuration_value('RABBITMQ_PORT', '5672'))
    RABBITMQ_MANAGER_PORT = int(get_configuration_value('RABBITMQ_MANAGER_PORT', '15672'))
    RABBITMQ_VHOST = get_configuration_value('RABBITMQ_VHOST', '')
    RABBITMQ_PASSWORD = get_configuration_value('RABBITMQ_PASSWORD', 'rabbitmq')


class RotatingFileLogger(BaseConfig):
    USE_FILE_ROTATING_LOG = get_configuration_value('USE_FILE_ROTATING_LOG', True)
    FILE_HANDLER = None
    if USE_FILE_ROTATING_LOG:
        LOGS_FOLDER = get_configuration_value('LOGS_FOLDER', '/logs')
        log_rotate_max_bytes = int(get_configuration_value('LOG_ROTATE_MAX_BYTES', 20971520))
        log_rotate_backup_count = int(get_configuration_value('LOG_ROTATE_BACKUP_COUNT', 5))
        log_level = get_configuration_value('LOG_LEVEL', 'INFO')
        LOG_LEVEL = getattr(logging, log_level.upper())
        log_file = get_configuration_value('LOG_FILE', 'tesla_admin.log')

        formatter = logging.Formatter('%(asctime)s - %(processName)s - %(levelname)s - %(message)s')

        # File logger
        try:
            if not os.path.exists(LOGS_FOLDER):
                os.makedirs(LOGS_FOLDER)
        except OSError:
            print("Cannot create logs folder at {}. Using './logs' instead".format(LOGS_FOLDER))
            LOGS_FOLDER = './logs'
            if not os.path.exists(LOGS_FOLDER):
                os.makedirs(LOGS_FOLDER)

        file_handler = RotatingFileHandler(os.path.join(LOGS_FOLDER, log_file), maxBytes=log_rotate_max_bytes,
                                           backupCount=log_rotate_backup_count)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(LOG_LEVEL)

        FILE_HANDLER = file_handler


class ESLoggerConfig(BaseConfig):
    USE_ELASTIC_SEARCH = bool(get_configuration_value('USE_ES_LOGS', False))
    ES_HANDLER = None
    if USE_ELASTIC_SEARCH:
        from cmreslogging.handlers import CMRESHandler
        es_host = get_configuration_value('ES_HOST', 'localhost')
        es_port = int(get_configuration_value('ES_PORT', 9200))
        es_user = get_configuration_value('ES_USER', None)
        es_password = get_configuration_value('ES_PASSWORD', None)
        es_use_ssl = bool(int(get_configuration_value('ES_USE_SSL', 0)))
        es_verify_ssl = get_configuration_value('ES_VERIFY_SSL', False)
        es_index_name = get_configuration_value('ES_INDEX_NAME', 'tesla_admin_index')
        es_auth_type = CMRESHandler.AuthType.NO_AUTH
        if es_user is not None and es_password is not None:
            es_auth_type = CMRESHandler.AuthType.BASIC_AUTH

        es_handler = CMRESHandler(hosts=[{'host': es_host, 'port': es_port}],
                                  auth_type=es_auth_type,
                                  auth_details=(es_user, es_password),
                                  use_ssl=es_use_ssl,
                                  verify_ssl=es_verify_ssl,
                                  es_index_name=es_index_name,
                                  flush_frequency_in_sec=15,
                                  es_additional_fields={
                                      'Module': BaseConfig.MODULE_NAME,
                                      'Version': BaseConfig.MODULE_VERSION,
                                      'Environment': BaseConfig.CONFIG_NAME
                                  })
        if es_handler.test_es_source():
            es_handler.setLevel(logging.INFO)
            ES_HANDLER = es_handler


class StdOutLogger(BaseConfig):
    USE_STDOUT = bool(get_configuration_value('USE_STDOUT', True))
    if USE_STDOUT:
        formatter = logging.Formatter('%(asctime)s - %(processName)s - %(levelname)s - %(message)s')
        stdout = logging.StreamHandler(sys.stdout)
        stdout.setLevel(logging.DEBUG)
        stdout.setFormatter(formatter)
        STDOUT_HANDLER = stdout


class CeleryConfig(RabbitConfig, DBConfig):
    rabbitmq_url = 'amqp://{}:{}@{}/{}'
    result_backend_format = 'db+postgresql://{}:{}@{}:{}/{}'

    # Setup Celery
    USE_CELERY = bool(int(get_configuration_value('USE_CELERY', 1)))
    CELERY_TIMEZONE = 'Europe/Berlin'
    CELERY_BROKER_URL = rabbitmq_url.format(RabbitConfig.RABBITMQ_USER, RabbitConfig.RABBITMQ_PASSWORD,
                                            RabbitConfig.RABBITMQ_HOST + ':' + str(RabbitConfig.RABBITMQ_PORT),
                                            RabbitConfig.RABBITMQ_VHOST)
    CELERY_RESULT_BACKEND = result_backend_format.format(DBConfig.DB_USER, DBConfig.DB_PASSWORD,
                                                         DBConfig.DB_HOST, DBConfig.DB_PORT, DBConfig.DB_NAME)
    CELERY_SEND_TASK_SENT_EVENT = True

    result_backend = CELERY_RESULT_BACKEND
    task_track_started = True
    result_persistent = True
    task_reject_on_worker_lost = True


class SecurityConfig():
    # Default Admin
    ADMIN_MAIL = get_configuration_value('ADMIN_MAIL', 'admin@tesla-project.eu')
    ADMIN_PASSWORD = get_configuration_value('ADMIN_PASSWORD', 'admin')

    # Flask-User settings
    SECURITY_TRACKABLE = True
    SECURITY_USER_IDENTITY_ATTRIBUTES = ('email', 'username')
    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_SALT = BaseConfig.SECRET_KEY
    # SECURITY_CONFIRMABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    #SECURITY_POST_LOGIN_VIEW = 'index'
    #SECURITY_POST_LOGOUT_VIEW = 'index'
    #SECURITY_POST_REGISTER_VIEW = 'index'
    SECURITY_EMAIL_SENDER = 'TeSLA Administration Portal <tesla@admin_portal.eu>'


class MailConfig():
    # Flask-Mail SMTP server settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False

    # Flask-Mail SMTP account settings
    MAIL_USERNAME = 'email@example.com'
    MAIL_PASSWORD = 'password'


class TEPConfig(BaseConfig):
    connection_url = '{}://{}:{}@{}:{}/{}'

    # TEP configuration
    TEP_URL = get_configuration_value('TEP_URL', 'https://localhost')
    TEP_PORT = int(get_configuration_value('TEP_PORT', 443))

    TEP_DB_USER = get_configuration_value('TEP_DB_USER', None)
    TEP_DB_HOST = get_configuration_value('TEP_DB_HOST', 'localhost')
    TEP_DB_PORT = get_configuration_value('TEP_DB_PORT', 5432)
    TEP_DB_NAME = get_configuration_value('TEP_DB_NAME', 'tesla_tep')
    TEP_DB_PASSWORD = get_configuration_value('TEP_DB_PASSWORD', None)
    TEP_DB_ENGINE = get_configuration_value('TEP_DB_ENGINE', 'postgresql')

    TEP_SQLALCHEMY_DATABASE_URI = connection_url.format(TEP_DB_ENGINE, TEP_DB_USER, TEP_DB_PASSWORD,
                                                        TEP_DB_HOST, TEP_DB_PORT, TEP_DB_NAME)

    TIP_URL = get_configuration_value('TIP_URL', None)
    TIP_PORT = get_configuration_value('TIP_PORT', 443)
    if TEP_URL.startswith("https://tep.") and TIP_URL is None:
        TIP_URL = TEP_URL.replace("https://tep.", "https://tip.")
    if TIP_URL is not None and not TIP_URL.endswith('/'):
        TIP_URL += '/'


class Config(SecurityConfig, MailConfig, StdOutLogger, ESLoggerConfig, CeleryConfig, RotatingFileLogger, TEPConfig):
    # CHECK FOR DANGEROUS SETTINGS
    SKIP_CERT_VERIFICATION = bool(int(get_configuration_value('SKIP_CERT_VERIFICATION', 0)))

    # Babel configuration
    SUPPORTED_LANGUAGES = {'ca_ES': 'Catalan', 'bg_BG': 'Bulgarian', 'en_GB': 'English', 'fr_FR': 'Français',
                           'es_ES': 'Spanish'}
    BABEL_DEFAULT_LOCALE = 'en_GB'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

    # Setup instrument
    BUNDLE_ERRORS = True
    TMP_PATH = get_configuration_value('TMP_PATH', '/tmp')
    INSTRUMENT_PORT = int(get_configuration_value('INSTRUMENT_PORT', 5000))
    CERT_PATH = get_configuration_value('CERT_PATH', '/run/secrets/')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}