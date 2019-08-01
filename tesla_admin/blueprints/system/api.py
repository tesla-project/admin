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

from flask import Blueprint, jsonify
from tesla_admin import tesla_data_provider
from tesla_admin.errors import not_found
from flask_security import roles_required, login_required
from tesla_admin.decorators import certificate_required, token_required
from tesla_admin import tesla_db, logger
from tesla_admin.blueprints.system.cawrapper.certificate import get_x509_cerificate
from flask import request
from tesla_admin.git_config import get_config_repository

import time, json, jwt, os

api_system = Blueprint('api_system', __name__)


@api_system.route('/config/<string:version>', methods=['GET'])
@certificate_required(subject_cert=True)
def module_config(subject_cert=None, version=None):
    # GET -> version, submodule, module
    # module [optional]: database, rabbit, redis, tep, tip , lti, rt ...
    # submodule: database, rabbit, redis, tep, tip, lti , rf...
    # version [optional]:

    module_acronym = request.args.get('module')
    if module_acronym is None:
        module_acronym = subject_cert.OU.lower()

    if module_acronym.find('broker') != -1:
        module_acronym = 'broker'

    submodule_acronym = request.args.get('submodule')

    try:
        environment = get_config_repository().get_module_config(module_acronym).get_config()
        return jsonify(environment), 200
    except:
        return not_found('Configuration for this module not found')


@api_system.route('/certificate/<string:module>/<string:type>', methods=['GET'])
@token_required
def module_certificate(module, type, service=None):
    # module = ['SERVER', 'CLIENT']
    # type = ['CA', 'CERTIFICATE', 'KEY']
    # header TESLA_TOKEN -> acronym
    # header X-TESLA: instrument (tesla_token)
    institution = "UOC"
    country = "ES"
    module = module.upper()

    if module != 'SERVER' and module != 'CLIENT':
        return jsonify("Module value is not correct"), 400, {'Content-Type': 'text/plain; charset=utf-8'}

    type = type.upper()
    if type != 'CA' and type != 'CERTIFICATE' and type != 'KEY':
        return jsonify("Type value is not correct"), 400, {'Content-Type': 'text/plain; charset=utf-8'}

    try:
        logger.debug("Getting certificate for service: "+str(service)+" module "+str(module)+" type "+str(type))
        cert = get_x509_cerificate(service, certificate_type=module, key_or_cert=type)
        logger.debug(str(cert))
    except Exception as e:
        logger.error(str(e))
        return jsonify("Error unkown"), 500, {'Content-Type': 'text/plain; charset=utf-8'}

    return str(cert), 200, {'Content-Type': 'text/plain; charset=utf-8'}


@api_system.route('/certificate/tep', methods=['GET'])
@certificate_required(subject_cert=True)
def module_certificate_tep(subject_cert=None):
    return_data = {}
    try:
        logger.debug("Getting certificate for service: tep module")
        key = get_x509_cerificate("tep", certificate_type="CLIENT", key_or_cert="KEY")
        cert = get_x509_cerificate("tep", certificate_type="CLIENT", key_or_cert="CERT")
        ca = get_x509_cerificate("tep", certificate_type="CLIENT", key_or_cert="CA")
        return_data = {'key': key, 'cert': cert, 'ca': ca}
    except Exception as e:
        logger.error(str(e))
        return jsonify("Error unkown"), 500, {'Content-Type': 'text/plain; charset=utf-8'}

    return jsonify(return_data), 200, {'Content-Type': 'text/plain; charset=utf-8'}


# todo: remove this method in production
@api_system.route('/token/<string:module>', methods=['GET'])
def module_token(module):
    institution = "UOC"

    client_key = '/run/secrets/'+str(os.getenv('SECRET_PREFIX'))+'SERVER_KEY'

    with open(client_key, 'r') as key_file:
        secret = str(key_file.read())

    token = jwt.encode({'module': str(module), 'institution': str(institution)}, secret, 'RS256')

    return jsonify({"data": str(token.decode())}), 200, {'Content-Type': 'text/plain; charset=utf-8'}
