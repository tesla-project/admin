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
from OpenSSL import crypto
from tesla_admin import logger

AUTHORIZED_CLIENTS = ['tep', 'rt', 'plugin', 'tip', 'ks', 'tpt', 'fa', 'fr', 'fra', 'vr', 'vra', 'ts', 'broker',
                      'worker', 'beat', 'api', 'flower']


def validate_client_cert(cert, authorized=AUTHORIZED_CLIENTS):
    cert = clean_certificate(cert)

    try:
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
    except Exception as e:
        print(str(e))
    # logging.info('cert info: ' + str(cert))

    subject = cert.get_subject()

    # logging.info('subject: ' + str(subject))

    issued_to = subject.CN.lower()

    # logging.info('issued_to: ' + str(issued_to))
    if isinstance(authorized, str):
        is_valid = issued_to == authorized
    else:
        is_valid = any([issued_to.startswith(client) for client in authorized])

    if not is_valid:
        logger.warning("Certificate validation failed: got {} compared to {}".format(issued_to, authorized))

    return is_valid


def get_secret(secret_name, default=None):
    secret_filename = os.path.join('/run/secret/', secret_name)

    if os.path.isfile(secret_filename):
        with open(secret_filename, 'r') as content_file:
            content = content_file.read()
            return content
    else:
        return os.getenv(secret_name, default)


def get_subject_cert(cert):
    cert = clean_certificate(cert)
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert)

    return cert.get_subject()


def clean_certificate(cert):
    cert = cert.replace('-----BEGIN CERTIFICATE-----', '-----BEGINCERTIFICATE-----')
    cert = cert.replace('-----END CERTIFICATE-----', '-----ENDCERTIFICATE-----')
    cert = cert.replace(' ', '\n')
    cert = cert.replace('-----BEGINCERTIFICATE-----', '-----BEGIN CERTIFICATE-----')
    cert = cert.replace('-----ENDCERTIFICATE-----', '-----END CERTIFICATE-----')
    cert = cert + '\n'

    return cert
