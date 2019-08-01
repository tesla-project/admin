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

from minio import Minio
from minio.error import ResponseError
import io

class DataStorage(object):

    def __init__(self, logger):
        super(DataStorage, self).__init__()

        self.logger = logger

    def save_request_data(self, request_id, data):
        return 1

    def save_request_audit_data(self, request_id, instrument_id, with_enrolment, with_request, data):
        return 1

    def save_learner_model(self, tesla_id, instrument_id, model):
        return 1

    def load_request_data(self, request_id):
        return None

    def load_request_audit_data(self, request_id, instrument_id):
        return None

    def load_learner_model(self, tesla_id, instrument_id):
        return None


class DBDataStorage(DataStorage):

    def __init__(self, logger, db):
        super(DBDataStorage, self).__init__(logger)

        self.db = db

    def save_request_data(self, request_id, data):
        bin_data = data.encode()
        new_req = self.db.requests.create_request_data(request_id, bin_data)
        if new_req is None:
            return 1
        return 0

    def save_request_audit_data(self, request_id, instrument_id, with_enrolment, with_request, data):
        bin_data = None
        if data is not None:
            bin_data = data.encode()
        new_data = self.db.requests.create_update_request_result_audit_data(request_id=request_id, instrument_id=instrument_id,
                                                                   with_enrolment=with_enrolment, with_request=with_request,
                                                                   data=bin_data)
        if new_data is None:
            return 1
        return 0

    def save_learner_model(self, tesla_id, instrument_id, model):
        return 1

    def load_request_data(self, request_id):
        bin_data = self.db.requests.get_request_data(request_id)
        return bin_data.data.decode()

    def load_request_audit_data(self, request_id, instrument_id):
        audit = self.db.requests.get_request_result_audit(request_id, instrument_id)
        audit_data = audit.data.decode()
        return {'enrolment': audit.enrolment, 'request': audit.request, 'audit_data': audit_data}

    def load_learner_model(self, tesla_id, instrument_id):
        return None


class MinioDataStorage(DataStorage):

    def __init__(self, logger, host, port, access_key, secret_key, secure=False):
        super(MinioDataStorage, self).__init__(logger)

        self.client = Minio('{}:{}'.format(host, port), secret_key=secret_key, access_key=access_key, secure=secure)

    def save_request_data(self, request_id, data):
        bin_data = data.encode()
        raw = io.BytesIO(bin_data)
        raw.seek(0)

        if not self.client.bucket_exists('requests'):
            self.client.make_bucket('requests')

        try:
            self.client.put_object('requests', '{}_data.bin'.format(request_id), raw, len(bin_data))
        except Exception:
            return 1

        return 0

    def save_request_audit_data(self, request_id, instrument_id, with_enrolment, with_request, data):
        raw = io.BytesIO(data)
        raw.seek(0)

        if not self.client.bucket_exists('requests'):
            self.client.make_bucket('requests')

        try:
            self.client.put_object('requests', '{}_audit.bin'.format(request_id), raw, len(data))
        except Exception:
            return 1

        return 0

    def save_learner_model(self, tesla_id, instrument_id, model):
        return 1

    def load_request_data(self, request_id):
        bin_data = self.client.get_object("requests", '{}_data.bin'.format(request_id))
        return bin_data.decode()

    def load_request_audit_data(self, request_id, instrument_id):

        return self.db.requests.get_request_result_audit(request_id, instrument_id)

    def load_learner_model(self, tesla_id, instrument_id):
        return None