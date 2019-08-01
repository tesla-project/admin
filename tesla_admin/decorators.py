"""
TeSLA function decorators
"""
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

from functools import wraps
from flask import request, jsonify
from tesla_admin import secret
import os

from tesla_admin import logger


def drain_request():
    """
    Helper function that will trigger a dummy call to consume post data because
    the requests package fails to handle early "termination".
    see https://github.com/kennethreitz/requests/issues/2422 for a related issue
    """
    request.get_json(silent=True, cache=False)


def certificate_required(subject_cert=False):
    """
    This route decorator applies certification validation before going further.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            validated = False
            try:
                if subject_cert is True:
                    kwargs['subject_cert'] = None

                authorized_clients = secret.AUTHORIZED_CLIENTS
                skip_cert_verification = bool(os.environ.get('SKIP_CERT_VERIFICATION', 0))
                if skip_cert_verification:
                    validated = True
                    return f(*args, **kwargs)

                client_cert = request.environ.get('HTTP_X_SSL_CERT', None)

                if not client_cert or not secret.validate_client_cert(client_cert, authorized_clients):
                    drain_request()
                    return jsonify({'status_code': '54'}), 401  # code 54 for invalid client_cert

                if subject_cert is True:
                    kwargs['subject_cert'] = secret.get_subject_cert(cert=client_cert)

                validated = True
                return f(*args, **kwargs)

            except Exception as ex:
                if not validated:
                    return jsonify({'status_code': '54'}), 401  # code 54 for invalid client_cert
                else:
                    raise ex

        return decorated_function
    return decorator


def token_required(f):
    """
    This route decorator applies token validation before going further.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        validated = False
        try:
            '''
            authorized_clients = secret.AUTHORIZED_CLIENTS
            skip_cert_verification = bool(os.environ.get('SKIP_CERT_VERIFICATION', 0))
            if skip_cert_verification:
                validated = True
                return f(*args, **kwargs)

            client_cert = request.environ.get('HTTP_X_SSL_CERT', None)

            if not client_cert or not secret.validate_client_cert(client_cert, authorized_clients):
                drain_request()
                return jsonify({'status_code': '54'}), 401  # code 54 for invalid client_cert
            '''

            x_tesla = request.headers.get('Authorization', '')
            service = x_tesla.replace('X-TESLA', '').replace(' ', '')

            kwargs['service'] = service

            return f(*args, **kwargs)
        except Exception as ex:
            if not validated:
                return jsonify({'status_code': '54'}), 401  # code 54 for invalid client_cert
            else:
                raise ex

    return decorated_function