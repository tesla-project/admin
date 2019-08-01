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
import requests


class TIP():

    def __init__(self, config, logger):
        self.tip_url = config['TIP_URL']
        self.cert_path = config['CERT_PATH']
        self.logger = logger

    def get_tesla_id(self, mail):
        url = '{0}users/id'.format(self.tip_url)

        data = {
            "mail": mail
        }

        try:
            prefix = os.getenv('SECRET_PREFIX', '')

            response = requests.post(url, json=data,
                                    verify=os.path.join(self.cert_path, prefix + 'CLIENT_CA'),
                                    cert=(os.path.join(self.cert_path, prefix + 'CLIENT_CERT'),
                                          os.path.join(self.cert_path, prefix + 'CLIENT_KEY')))

            if response.status_code != 200:
                self.logger.error('Error requesting tesla_id to TIP. status_code = {}'.format(response.status_code))
                return False, None
            else:
                response_json = response.json()

            #valid, valid_data, errors = validators.validate_portal_instruments(response_json)

            #if not valid:
            #    self.logger.debug("Invalid Instruments data provided by portal:\n\n{}".format(errors))

            valid = True
            tesla_id = response_json['tesla_id']

        except Exception as exception:
            self.logger.exception("Error parsing list of instruments from Portal")
            return False, str(exception)

        return valid, tesla_id

    def exists(self, mail):
        url = '{0}users/check/mail'.format(self.tip_url)

        data = {
            "mail": mail
        }

        try:
            prefix = os.getenv('SECRET_PREFIX', '')

            response = requests.post(url, json=data,
                                    verify=os.path.join(self.cert_path, prefix + 'CLIENT_CA'),
                                    cert=(os.path.join(self.cert_path, prefix + 'CLIENT_CERT'),
                                          os.path.join(self.cert_path, prefix + 'CLIENT_KEY')))

            if response.status_code != 200:
                self.logger.error('Error requesting tesla_id to TIP. status_code = {}'.format(response.status_code))
                return False, None
            else:
                response_json = response.json()

            #valid, valid_data, errors = validators.validate_portal_instruments(response_json)

            #if not valid:
            #    self.logger.debug("Invalid Instruments data provided by portal:\n\n{}".format(errors))

            result = bool(response_json['result'])

        except Exception as exception:
            self.logger.exception("Error parsing list of instruments from Portal")
            return False

        return result
