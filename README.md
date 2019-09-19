# TeSLA Administration (ADMIN)

---

## Synopsis
The TeSLA Administration is a module that manage the institution part of TeSLA.

---

## Configuration

The environment variables used by ADMIN are:

###  General Admin configuration 
	* SECRET_KEY=secret_key
	* DEBUG=False
	* CONFIG=production
	* SECRET_PREFIX=secret_prefix
	* TMP_PATH=/tmp
	* CERT_PATH=/run/secrets/
	* USE_REDIS=0
	* COUNTRY=ES
	* MODULE_NAME=ADMIN
	* DOMAIN=domain.tesla-project.eu
	* INSTITUTION=institution acronym

### Enable or disable the use of local JS and CSS
	* USE_LOCAL_LIBS=0

### Logging options
	* LOG_LEVEL=INFO
	* USE_FILE_ROTATING_LOG=1
	* LOGS_FOLDER=/logs
	* LOG_ROTATE_MAX_BYTES=20971520
	* LOG_ROTATE_BACKUP_COUNT=5
	* LOG_FILE=tesla_admin.log
	* USE_ES_LOGS=0
	* USE_STDOUT=1

### Celery properties
	* USE_CELERY=1
	* CELERY_TIMEZONE = 'Europe/Berlin'

### Initial administration account
	* ADMIN_MAIL = 'xbaro@uoc.edu'
	* ADMIN_PASSWORD = 'admin'

### Database
	* DB_PORT=5432
	* DB_USER=db_user
	* DB_NAME=db_name
	* DB_PASSWORD=db_password
	* DB_HOST=db_host
	* DB_SCHEMA=db_schema

### TEP Database
	* TEP_DB_NAME=tep_db_name
	* TEP_DB_HOST=tep_db_host
	* TEP_DB_PASSWORD=tep_db_password
	* TEP_DB_USER=tep_db_user
	* TEP_DB_PORT=tep_db_port
	* TEP_DB_ENGINE=tep_db_engine

### Git repository configuration
	* USE_GIT_CONFIG=0
	* GIT_WORKING_PATH=./data_admin/conf_repo/
	* GIT_USER=git_user
	* GIT_PASSWORD=git_password
	* GIT_REPOSITORY=git_repository

### Rabbit MQ configuration
	* RABBITMQ_PASSWORD=RABBIT_PASSWORD
	* RABBITMQ_MANAGER_PORT=15672
	* RABBITMQ_PORT=5672
	* RABBITMQ_USER=RABBIT_USER
	* RABBITMQ_VHOST=/
	* RABBITMQ_HOST=rabbit

### TIP configuration
	* TIP_URL=https://tipurl.eu

---


## Installation

.env file has all the environment variables used by the ADMIN, and docker-compose configuration file shows how to setup an instance of the ADMIN and required database.

Docker compose assigns the .env variables to different containers.



---

## Contributors
- Xavier Baró <xbaro@uoc.edu>
- Roger Muñoz <rmunozber@uoc.edu>
- David Gañan <dganan@uoc.edu>

---
## License
This software is released under AGPL-3.0 license
