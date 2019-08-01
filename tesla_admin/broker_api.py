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

import requests

class TeSLABroker:

    def __init__(self, broker_url, broker_port, api_base='/api/v1/'):
        self.broker_base = '{}:{}{}'.format(broker_url, broker_port, api_base)
        self.broker = requests.Session()
        #self.broker.cert = ('/path/client.cert')

        self.categories = []

    def get_instrument_stats(self):
        try:
            resp = self.broker.get('{}stats/instruments/status'.format(self.broker_base))

            if resp.status_code != 200:
                return []

            ret_value = resp.json()
            if int(ret_value['status_code']) != 0:
                return []
        except:
            return []

        return ret_value['instruments']

    def get_send_categories(self):
        try:
            resp = self.broker.get('{}send/categories'.format(self.broker_base))

            if resp.status_code != 200:
                return []

            ret_value = resp.json()
            if int(ret_value['status_code']) != 0:
                return []
        except:
            return []

        return ret_value['categories']

    def create_send_category(self, data):
        return []

    def update_send_category(self, data):
        return []