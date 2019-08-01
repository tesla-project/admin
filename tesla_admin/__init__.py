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
from werkzeug.local import LocalProxy
from flask import Flask, render_template, g, request
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_migrate import Migrate
from flask_cors import CORS
from celery import Celery
from flask_babelex import Babel
from flask_security import Security, SQLAlchemySessionUserDatastore, current_user
from flask_security.utils import hash_password
from flask_jsglue import JSGlue
from flask_marshmallow import Marshmallow
import atexit
import logging
from datetime import datetime

celery = None
db = None
logger = None

# Execute final tasks before exit
def exit_handler():
    if logger is not None:
        logger.warning("Exiting application")
    if celery is not None:
        celery.close()
    if logger is not None:
        for h in app.logger.handlers:
            h.flush()
            h.close()


atexit.register(exit_handler)

from tesla_admin.config import config as config_env

# If the environment is not defined, assume production
config_name = os.environ.get('CONFIG', 'production')
current_config = config_env[config_name]
config = LocalProxy(lambda: current_config)

# Create the Flask application
app = Flask(__name__)
app.config.from_object(current_config)
moment = Moment(app)
jsglue = JSGlue(app)

# accepts requests from all sources, may change in future for security reasons
cors = CORS(app, resources={r"*": {"origins": "*"}})

# Setup Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)
celery.config_from_object(app.config)

# Setup the logger
root_logger = logging.getLogger()
root_logger.setLevel(app.config['LOG_LEVEL'])
app.logger.setLevel(app.config['LOG_LEVEL'])
if app.config['USE_FILE_ROTATING_LOG']:
    app.logger.addHandler(app.config['FILE_HANDLER'])
    root_logger.addHandler(app.config['FILE_HANDLER'])
if app.config['USE_STDOUT']:
    app.logger.addHandler(app.config['STDOUT_HANDLER'])
    root_logger.addHandler(app.config['STDOUT_HANDLER'])
if app.config['USE_ELASTIC_SEARCH']:
    es_handler = app.config['ES_HANDLER']
    if app.config['ES_HANDLER'] is not None:
        app.logger.addHandler(app.config['ES_HANDLER'])
        root_logger.addHandler(app.config['ES_HANDLER'])
    else:
        app.logger.warning("Elastic Search logger enabled, but cannot contact with Elastic Search Server. ES logger disabled.")
logger = LocalProxy(lambda: app.logger)  # type: app.logger

# Connect with SQLAlchemy
from tesla_models import init_tesla_db
tesla_db = init_tesla_db(app)
migrate = Migrate(app, tesla_db.db)
ma = Marshmallow(app)

# setup Babel internationalization
babel = Babel(app)

@babel.localeselector
def get_locale():
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    if current_user is not None and current_user.is_authenticated:
        return current_user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.
    return request.accept_languages.best_match(app.config['SUPPORTED_LANGUAGES'])

@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone
    if current_user is not None and current_user.is_authenticated:
        return current_user.timezone
    return app.config['BABEL_DEFAULT_TIMEZONE']

# Define the Login middlewere
from tesla_models.models import User, Role
from tesla_admin.forms import ExtendedRegisterForm
user_datastore = SQLAlchemySessionUserDatastore(tesla_db.db.session, User, Role)
security = Security(app=app, datastore=user_datastore, register_form=ExtendedRegisterForm)

@app.before_first_request
def create_user():
    # Ensure that admin user is created
    admin_role = user_datastore.find_or_create_role(name="Admin", description="TeSLA Administrator")
    admin = user_datastore.find_user(username="admin")
    if admin is None:
        admin = user_datastore.create_user(username="admin", email=app.config['ADMIN_MAIL'],
                                           password=hash_password(app.config['ADMIN_PASSWORD']),
                                           locale=app.config['BABEL_DEFAULT_LOCALE'],
                                           timezone=app.config['BABEL_DEFAULT_TIMEZONE'])
        user_datastore.add_role_to_user(admin, admin_role)

    # Create roles
    user_datastore.find_or_create_role(name="SEND_Admin", description="Allows to manage SEND information")
    user_datastore.find_or_create_role(name="Data", description="Allows to manage learners data")
    user_datastore.find_or_create_role(name="InformedConsent", description="Allows to manage Informed Consents")
    user_datastore.find_or_create_role(name="Statistics", description="Allows to see statistical data")

    tesla_db.db.session.commit()


# Check for dangerous settings
if app.config['SKIP_CERT_VERIFICATION']:
    logger.warning('Skip Certificate verification is ACTIVATED. On production set SKIP_CERT_VERIFICATION=0')

# Register default error handlers
from tesla_models.errors import not_found, access_denied, internal_error
app.register_error_handler(404, not_found)
app.register_error_handler(401, access_denied)
app.register_error_handler(500, internal_error)

# Register index page
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', page = 'home')

# Import the TIP API connection objects
from .tip_api import TIP
tip_api_connect = LocalProxy(lambda: TIP(config=app.config, logger=logger))  # type: TIP

# Add default information for templates
from tesla_admin.data_provider import TeSLADataProvider
tesla_data_provider = TeSLADataProvider()

@app.context_processor
def inject_alerts():
    option_local_libs = app.config['USE_LOCAL_LIBS']
    if current_user.is_authenticated:
        return dict(user=current_user,
                    option_local_libs = option_local_libs,
                    messages=tesla_data_provider.get_messages(),
                    notifications=tesla_data_provider.get_notifications())
    return dict(user=current_user, option_local_libs=option_local_libs)

# Add tesla administration blueprint
api_base = '/api/v1'
from tesla_admin.api import api_learner as tesla_admin_api_learner
app.register_blueprint(tesla_admin_api_learner, url_prefix=api_base + '/learner')

# Add User management blueprint
from tesla_admin.blueprints.users.routes import users
app.register_blueprint(users, url_prefix='/users')

# Add Informed Consent blueprint
from tesla_admin.blueprints.informed_consent.routes import informed_consent
app.register_blueprint(informed_consent, url_prefix='/informed_consent')

# Add Data management blueprint
from tesla_admin.blueprints.data.routes import data
app.register_blueprint(data, url_prefix='/data')

# Add SEND blueprint
from tesla_admin.blueprints.send.routes import send
app.register_blueprint(send, url_prefix='/send')

# Add admin api system
from tesla_admin.blueprints.system.api import api_system
app.register_blueprint(api_system, url_prefix=api_base + '/system')

# Add System blueprint
from tesla_admin.blueprints.system.routes import system
app.register_blueprint(system, url_prefix='/system')

# Add statistics blueprint
from tesla_admin.blueprints.stats.routes import stats
app.register_blueprint(stats, url_prefix='/stats')

# Add Reports blueprint
from tesla_admin.blueprints.report.routes import reports
app.register_blueprint(reports, url_prefix='/reports')