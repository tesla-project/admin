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

from tesla_models.models import TiesService, TiesConfig, TiesResult
from tesla_models.constants import TIES_RESULT_STATUS
from sqlalchemy import asc, desc, or_, func
import uuid


class TiesDB(object):

    def __init__(self, db, logger):
        self.logger = logger
        self.db = db

    def create_service(self, code, name, key, secret, base_url, active):
        try:

            ties_service = TiesService(code=code, name=name, key=key, secret=secret, base_url=base_url, active=active)

            self.db.session.add(ties_service)
            self.db.session.commit()
            self.db.session.refresh(ties_service)
        except Exception:
            self.logger.exception("Error creating new service {}".format(ties_service))
            ties_service = None

        return ties_service

    def get_service(self, code):
        ties_service = None

        try:
            ties_service = TiesService.query.filter_by(code=code).one_or_none()
        except Exception:
            self.logger.exception("Error getting ties_service with code {}".format(code))

        return ties_service

    def get_all_services(self):
        ties_services = []
        try:
            ties_services = TiesService.query.all()
        except Exception:
            self.logger.exception("Error getting all ties_service")

        return ties_services

    def update_service(self, code, name=None, key=None, secret=None, base_url=None, active=None):
        ties_service = self.get_service(code)

        try:
            if ties_service is not None:
                data = {}

                if name is not None:
                    data['name'] = name

                if key is not None:
                    data['key'] = key

                if secret is not None:
                    data['secret'] = secret

                if base_url is not None:
                    data['base_url'] = base_url

                if active is not None:
                    data['active'] = active

                TiesService.query.filter_by(code=code).update(data)
                self.db.session.commit()

        except Exception:
            self.logger.exception("Error updating ties_service for code {}".format(code))

        return ties_service

    def delete_service(self, code):
        try:
            ties_service = self.get_service(code=code)
            TiesResult.query.filter_by(service_id=ties_service.id).delete()
            self.db.session.commit()

            TiesService.query.filter_by(code=code).delete()
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error deleting ties_service for code {}".format(code))
            return False

        return True

    def pending_request_by_service(self, service):
        try:
            count = TiesResult.query(func.count(TiesResult)).filter_by(service_id=service.id, status=TIES_RESULT_STATUS.RESULT_PENDING)
            return count
        except Exception:
            self.logger.exception("Error calculating pending request by service code {}".format(service.code))
            return None

    def last_request_processed_by_service(self, service):
        try:
            ties_result = TiesResult.query.filter_by(service_id=service.id, status=TIES_RESULT_STATUS.RESULT_END).order_by(desc(TiesResult.updated)).limit(1).one_or_null()
            return ties_result
        except Exception:
            self.logger.exception("Error calculating last request processed by service code {}".format(service.code))
            return None

    def total_requests_processed_by_service(self, service):
        try:
            count = TiesResult.query(func.count(TiesResult)).filter_by(service_id=service.id, status=TIES_RESULT_STATUS.RESULT_END)
            return count
        except Exception:
            self.logger.exception("Error calculating total requests processed by service code {}".format(service.code))
            return None

    def create_request(self, data, services, client):
        try:
            guid = str(uuid.uuid1())

            if not isinstance(data, bytes):
                data = bytes(data, 'utf-8')

            ties_request = TiesRequest(data=data, client=client, token=guid)

            self.db.session.add(ties_request)
            self.db.session.commit()
            self.db.session.refresh(ties_request)


            for service in services:
                service_obj = self.get_service(code=service)
                if service_obj is not None:
                    ties_result = TiesResult(request_id=ties_request.id, service_id=service_obj.id, status=TIES_RESULT_STATUS.RESULT_PENDING)
                    self.db.session.add(ties_result)
                    self.db.session.commit()
                    self.db.session.refresh(ties_result)

        except Exception:
            self.logger.exception("Error creating ties_request")
            ties_request = None

        return ties_request

    def get_request(self, token):
        ties_request = None
        try:
            ties_request = TiesRequest.query.filter_by(token=token).one_or_none()
        except Exception:
            self.logger.exception("Error getting request token {}".format(token))

        return ties_request

    def delete_request(self, token):
        try:
            ties_request = self.get_request(token=token)

            if ties_request is not None:
                TiesResult.query.filter_by(request_id=ties_request.id).delete()
                self.db.session.commit()

                TiesRequest.query.filter_by(id=ties_request.id).delete()
                self.db.session.commit()
        except Exception:
            self.logger.exception("Error deleting ties request with token {}".format(token))
            return False

        return True
