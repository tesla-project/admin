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

from tesla_admin import logger
class EnvClassify:
    tree = {
        "services": {
            "database": {
                "icon": "fa fa-database",
                "fields": [
                    {
                        "key": "DB_PORT",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "DB_USER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "DB_NAME",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "DB_PASSWORD",
                        "required": True,
                        "type": "password"
                    },
                    {
                        "key": "DB_HOST",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "DB_SCHEMA",
                        "required": True,
                        "type": "text"
                    },
                ]
            },
            "elasticsearch": {
                "icon": "fa fa-es",
                "fields": [
                    {
                        "key": "ES_HOST",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "ES_PORT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "ES_USER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "ES_PASSWORD",
                        "required": True,
                        "type": "password"
                    },
                    {
                        "key": "ES_USE_SSL",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "ES_VERIFY_SSL",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "ES_INDEX_NAME",
                        "required": True,
                        "type": "text"
                    },
                ]
            },
            "mail": {
                "icon": "fa fa-envelope",
                "fields": [
                    {
                        "key": "MAIL_SERVER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MAIL_PORT",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "MAIL_USE_SSL",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "MAIL_USE_TLS",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "MAIL_USERNAME",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MAIL_PASSWORD",
                        "required": True,
                        "type": "password"
                    }
                ]
            },
            "minio": {
                "icon": "fa fa-file",
                "fields": []
            },
            "portal": {
                "icon": "fa fa-file",
                "fields": [
                    {
                        "key": "PORTAL_URL",
                        "required": True,
                        "type": "text"
                    }
                ]
            },
            "rabbit": {
                "icon": "fa fa-file",
                "fields": [
                    {
                        "key": "RABBITMQ_PASSWORD",
                        "required": True,
                        "type": "password"
                    },
                    {
                        "key": "RABBITMQ_MANAGER_PORT",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "RABBITMQ_PORT",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "RABBITMQ_USER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "RABBITMQ_VHOST",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "RABBITMQ_HOST",
                        "required": True,
                        "type": "text"
                    }
                ]
            },
            "redis": {
                "icon": "fa fa-file",
                "fields": [
                    {
                        "key": "REDIS_HOST",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "REDIS_PORT",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "REDIS_USER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "REDIS_PASSWORD",
                        "required": True,
                        "type": "password"
                    },
                    {
                        "key": "REDIS_DB",
                        "required": True,
                        "type": "integer"
                    }
                ]
            },
            "rt": {
                "icon": "fa fa-file",
                "fields": [
                    {
                        "key": "RT_URL",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "RT_PORT",
                        "required": True,
                        "type": "integer"
                    }
                ]
            },
            "tep": {
                "icon": "fa fa-file",
                "fields": [
                    {
                        "key": "TEP_URL",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "TEP_PORT",
                        "required": True,
                        "type": "integer"
                    }
                ]
            },
            "tep_db": {
                "icon": "fa fa-database",
                "fields": [
                    {
                        "key": "TEP_DB_NAME",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "TEP_DB_HOST",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "TEP_DB_PASSWORD",
                        "required": True,
                        "type": "password"
                    },
                    {
                        "key": "TEP_DB_USER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "TEP_DB_PORT",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "TEP_DB_ENGINE",
                        "required": True,
                        "type": "text"
                    },
                ]
            },
            "tip": {
                "icon": "fa fa-file",
                "fields": [
                    {
                        "key": "TIP_URL",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "TIP_PORT",
                        "required": True,
                        "type": "integer"
                    }
                ]
            },
        },
        "modules": {
            "admin": {
                "icon": "fa fa-file",
                "fields": [
                    {
                        "key": "SECRET_KEY",
                        "required": True,
                        "type": "password"
                    },
                    {
                        "key": "DEBUG",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "CONFIG",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SECRET_PREFIX",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_LOCAL_LIBS",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "LOG_LEVEL",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_FILE_ROTATING_LOG",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "LOGS_FOLDER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "LOG_ROTATE_MAX_BYTES",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "LOG_ROTATE_BACKUP_COUNT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "LOG_FILE",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_ES_LOGS",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "USE_STDOUT",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "USE_CELERY",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "CELERY_TIMEZONE",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "ADMIN_MAIL",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "ADMIN_PASSWORD",
                        "required": True,
                        "type": "password"
                    },
                    {
                        "key": "SKIP_CERT_VERIFICATION",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "TMP_PATH",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "CERT_PATH",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_REDIS",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "COUNTRY",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MODULE_NAME",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "DOMAIN",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "INSTITUTION",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MODULE_VERSION",
                        "required": True,
                        "type": "text"
                    }
                ]
            },
            "api": {
                "icon": "fa fa-file",
                "fields": [
                    {
                        "key": "SECRET_KEY",
                        "required": True,
                        "type": "password"
                    },
                    {
                        "key": "DEBUG",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "CONFIG",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SECRET_PREFIX",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_LOCAL_LIBS",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "LOG_LEVEL",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_FILE_ROTATING_LOG",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "LOGS_FOLDER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "LOG_ROTATE_MAX_BYTES",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "LOG_ROTATE_BACKUP_COUNT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "LOG_FILE",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_ES_LOGS",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "USE_STDOUT",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "USE_CELERY",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "CELERY_TIMEZONE",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "ADMIN_MAIL",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "ADMIN_PASSWORD",
                        "required": True,
                        "type": "password"
                    },
                    {
                        "key": "SKIP_CERT_VERIFICATION",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "TMP_PATH",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "CERT_PATH",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_REDIS",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "COUNTRY",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MODULE_NAME",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "DOMAIN",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "INSTITUTION",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MODULE_VERSION",
                        "required": True,
                        "type": "text"
                    }
                ]
            },
            "beat": {
                "icon": "fa fa-file",
                "fields": [
                    {
                        "key": "BROKER_COMPONENT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SECRET_KEY",
                        "required": True,
                        "type": "password"
                    },
                    {
                        "key": "DEBUG",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "CONFIG",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SECRET_PREFIX",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_LOCAL_LIBS",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "LOG_LEVEL",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_FILE_ROTATING_LOG",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "LOGS_FOLDER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "LOG_ROTATE_MAX_BYTES",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "LOG_ROTATE_BACKUP_COUNT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "LOG_FILE",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_ES_LOGS",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "USE_STDOUT",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "USE_CELERY",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "CELERY_TIMEZONE",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "ADMIN_MAIL",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "ADMIN_PASSWORD",
                        "required": True,
                        "type": "password"
                    },
                    {
                        "key": "SKIP_CERT_VERIFICATION",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "TMP_PATH",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "CERT_PATH",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_REDIS",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "COUNTRY",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MODULE_NAME",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "DOMAIN",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "INSTITUTION",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MODULE_VERSION",
                        "required": True,
                        "type": "text"
                    }
                ]
            },
            "flower": {
                "icon": "fa fa-file",
                "fields": [
                    {
                        "key": "BROKER_COMPONENT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SECRET_KEY",
                        "required": True,
                        "type": "password"
                    },
                    {
                        "key": "DEBUG",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "CONFIG",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SECRET_PREFIX",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_LOCAL_LIBS",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "LOG_LEVEL",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_FILE_ROTATING_LOG",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "LOGS_FOLDER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "LOG_ROTATE_MAX_BYTES",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "LOG_ROTATE_BACKUP_COUNT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "LOG_FILE",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_ES_LOGS",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "USE_STDOUT",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "USE_CELERY",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "CELERY_TIMEZONE",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "ADMIN_MAIL",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "ADMIN_PASSWORD",
                        "required": True,
                        "type": "password"
                    },
                    {
                        "key": "SKIP_CERT_VERIFICATION",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "TMP_PATH",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "CERT_PATH",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_REDIS",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "COUNTRY",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MODULE_NAME",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "DOMAIN",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "INSTITUTION",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MODULE_VERSION",
                        "required": True,
                        "type": "text"
                    }
                ]
            },
            "lti": {
                "icon": "fa fa-file",
                "fields": [
                    {
                        "key": "SERVER_CA",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SERVER_CERT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SERVER_KEY",
                        "required": True,
                        "type": "text"
                    }
                ]
            },
            "nginx-proxy": {
                "icon": "fa fa-file",
                "fields": [
                    {
                        "key": "DOMAIN",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "ENABLE_SERVICES",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "ENABLE_DOMAINS",
                        "required": True,
                        "type": "text"
                    }
                ]
            },
            "rt": {
                "icon": "fa fa-file",
                "fields": [
                    {
                        "key": "RT_LOGS_FOLDER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "RT_DEBUG",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "RT_PORT",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "RT_SSL_KEY",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "RT_SSL_CERT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "RT_SSL_CA_CERT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "RT_SSL_CLIENT_KEY",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "RT_SSL_CLIENT_CERT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "RT_SSL_CLIENT_CA_CERT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "RT_SSL_PATH",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "RT_USE_HTTP",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "RT_ISSUE_NAME",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "RT_AUTH_REQUESTS",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "RT_SEND_PUBLIC_KEY",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "RT_NUM_THREADS",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "RT_KEY_POOL_ENABLED",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "RT_KEY_POOL_SIZE",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "TEP_ADDRESS",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "DB_PORT",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "DB_USER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "DB_NAME",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "DB_PASSWORD",
                        "required": True,
                        "type": "password"
                    },
                    {
                        "key": "DB_HOST",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "DB_SCHEMA",
                        "required": True,
                        "type": "text"
                    },
                ]
            },
            "tep": {
                "icon": "fa fa-file",
                "fields": [
                    {
                        "key": "TEP_LOGS_FOLDER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "TEP_SEND_TO_DATAPROVIDER",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "TEP_DATA_PROVIDER_KEY",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "TEP_DATA_PROVIDER_SECRET",
                        "required": True,
                        "type": "password"
                    },
                    {
                        "key": "TEP_DATA_PROVIDER_SALT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "TEP_DATA_PROVIDER_API_BASE",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "TEP_PILOT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "TEP_DATA_PROVIDER_INSTITUTION",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "TEP_DEBUG",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "TEP_VERIFY_SSL_CERT",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "TEP_INTERNAL_PORT",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "TEP_EXTERNAL_PORT",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "TEP_PORTAL_URL_PORT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "TEP_SEND_STATS_TO_PORTAL",
                        "required": True,
                        "type": "boolean"
                    }
                ]
            },
            "fr": {
                "icon": "fa fa-file",
                "fields": [
                    {
                        "key": "SKIP_CERT_VERIFICATION",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "MODULE_NAME",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MODULE_VERSION",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "LOG_LEVEL",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "ENROLLMENT_MODE",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "INSTRUMENT_PORT",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "USE_STDOUT",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "LOGS_FOLDER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SECRET_PREFIX",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MAX_THREADS",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "USE_CELERY",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "SERVICE_CLASS",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "WORKER_CLASS",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "DATABASE_CLASS",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "INSTRUMENT_MODE",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_AUTO_CONFIG",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "AUTOMATIC_MIGRATIONS",
                        "required": True,
                        "type": "boolean"
                    }
                ]
            },
            "tfr": {
                "icon": "fa fa-file",
                "fields": [
                    {
                        "key": "INSTRUMENT_PORT",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "USE_STDOUT",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "LOGS_FOLDER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SECRET_PREFIX",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MAX_THREADS",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "USE_CELERY",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "SERVICE_CLASS",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "WORKER_CLASS",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "DATABASE_CLASS",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "INSTRUMENT_MODE",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_AUTO_CONFIG",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "AUTOMATIC_MIGRATIONS",
                        "required": True,
                        "type": "boolean"
                    }
                ]
            },
            "tip": {
                "icon": "fa fa-file",
                "fields": [
                    {
                        "key": "LOGS_FOLDER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "LOG_ROTATE_BACKUP_COUNT",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "LOG_ROTATE_MAX_BYTES",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "DEBUG",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "PORT",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "SSL_KEY",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SSL_CERT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SSL_CA_CERT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SSL_CLIENT_KEY",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SSL_CLIENT_CERT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SSL_CLIENT_CA_CERT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SSL_PATH",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_HTTP",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "ISSUE_NAME",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "AUTH_REQUESTS",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "SEND_PUBLIC_KEY",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "NUM_THREADS",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "MAX_MEM_THREAD",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "KEY_POOL_ENABLED",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "KEY_POOL_SIZE",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "TEP_ADDRESS",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MAX_TOKEN_VALIDITY",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "DISABLE_MAIL_VERIFICATION",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "SECRET_PREFIX",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "TEP_ENFORCE_KEY_SHARING",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "DB_PORT",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "DB_USER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "DB_NAME",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "DB_PASSWORD",
                        "required": True,
                        "type": "password"
                    },
                    {
                        "key": "DB_HOST",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "DB_SCHEMA",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "TOKEN_ISSUER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SERVER_CA",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SERVER_CERT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SERVER_KEY",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "CLIENT_CA",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "CLIENT_CERT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "CLIENT_KEY",
                        "required": True,
                        "type": "text"
                    }

                ]
            },
            "vle": {
                "icon": "fa fa-file",
                "fields": [
                    {
                        "key": "SERVER_CA",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SERVER_CERT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SERVER_KEY",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "PHPFPM_UPLOAD_MAX_FILESIZE",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "key": "NGINX_MAX_BODY_SIZE",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MOODLECFG_SSLPROXY",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MOODLE_WWWROOT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MOODLE_SUMMARY",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MOODLE_SHORTNAME",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MOODLE_FULLNAME",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MOODLE_DBUSER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MOODLE_DBPASS",
                        "required": True,
                        "type": "password"
                    },
                    {
                        "key": "MOODLE_DBNAME",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MOODLE_DBHOST",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MOODLE_ADMINUSER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MOODLE_ADMINPASS",
                        "required": True,
                        "type": "password"
                    },
                    {
                        "key": "MOODLE_ADMINEMAIL",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "CRON_MOODLE_INTERVAL",
                        "required": True,
                        "type": "integer"
                    }
                ]
            },
            "worker": {
                "icon": "fa fa-file",
                "fields": [
                    {
                        "key": "SECRET_KEY",
                        "required": True,
                        "type": "password"
                    },
                    {
                        "key": "DEBUG",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "CONFIG",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "SECRET_PREFIX",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_LOCAL_LIBS",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "LOG_LEVEL",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_FILE_ROTATING_LOG",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "LOGS_FOLDER",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "LOG_ROTATE_MAX_BYTES",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "LOG_ROTATE_BACKUP_COUNT",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "LOG_FILE",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_ES_LOGS",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "USE_STDOUT",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "USE_CELERY",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "CELERY_TIMEZONE",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "ADMIN_MAIL",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "ADMIN_PASSWORD",
                        "required": True,
                        "type": "password"
                    },
                    {
                        "key": "SKIP_CERT_VERIFICATION",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "TMP_PATH",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "CERT_PATH",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "USE_REDIS",
                        "required": True,
                        "type": "boolean"
                    },
                    {
                        "key": "COUNTRY",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MODULE_NAME",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "DOMAIN",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "INSTITUTION",
                        "required": True,
                        "type": "text"
                    },
                    {
                        "key": "MODULE_VERSION",
                        "required": True,
                        "type": "text"
                    }
                ]
            },
        }
    }

    def get_icon(self, type, service_name):
        service = self.tree[str(type)+"s"][service_name]
        return service['icon']

    def get_info(self, type, service_name, key):
        service = self.tree[str(type)+"s"][service_name]

        for field in service['fields']:
            if field['key'] == key:
                return field

        raise ValueError(str(type)+" "+str(service_name)+" "+key+" combination missing")