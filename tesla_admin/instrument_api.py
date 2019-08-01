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


class InstrumentAPI():

    def __init__(self, config, logger, instrument):
        self.instrument = instrument
        self.cert_path = config['CERT_PATH']
        self.admin_certs = 'data/certs/'
        self.logger = logger

    def get_activity_data(self, vle_id, activity_type, activity_id, tesla_id):
        external = False

        if external:
            inst_url = 'https://fr.inst.test.tesla-project.eu'
            inst_url = 'http://localhost:5000'
        else:
            inst_url = 'fr-service'

        url = '{}/activity/audit/{}/{}/{}/{}'.format(inst_url, vle_id, activity_id, activity_type, tesla_id)

        try:
            prefix = os.getenv('SECRET_PREFIX', '')
            if external:
                response = requests.get(url,
                                    verify=False,
                                    cert=(os.path.join(self.admin_certs, 'modules/tep', 'cert.pem'),
                                          os.path.join(self.admin_certs, 'modules/tep', 'key.pem')))
            else:
                response = requests.get(url,
                                    verify=os.path.join(self.admin_certs, 'deploy-manager', 'ca.pem'),
                                    cert=(os.path.join(self.admin_certs, 'modules/tep', 'cert.pem'),
                                          os.path.join(self.admin_certs, 'modules/tep', 'key.pem')))

            if response.status_code != 200:
                self.logger.error('Error requesting activity data to Instrument {}. status_code = {}'.format(self.instrument.id, response.status_code))
                return False, None
            else:
                response_json = response.json()

            valid = True
            audit = response_json['audit_data']

        except Exception as exception:
            self.logger.exception("Error parsing list of instruments from Instrument")
            return False, str(exception)

        return valid, audit
