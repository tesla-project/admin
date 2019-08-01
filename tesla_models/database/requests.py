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

from tesla_models.models import Request, RequestResult, RequestAudit, RequestData, Enrollment
from tesla_models.constants import TESLA_REQUEST_STATUS, TESLA_ENROLLMENT_PHASE, TESLA_RESULT_STATUS
from sqlalchemy import asc, desc, func
import json


class RequestDB(object):

    def __init__(self, db, logger):
        self.logger = logger
        self.db = db

    def is_enrollment(self, request_id):
        try:
            request = self.db.session.query(Request.is_enrolment).filter_by(id=request_id).one_or_none()
            ret_val = None
            if request is not None:
                ret_val = bool(request[0])
        except Exception:
            self.logger.exception("Error selecting request is_enrollment for request_id {}".format(request_id))
            ret_val = None

        return ret_val

    def finish_request(self, request_id, status=TESLA_REQUEST_STATUS.DONE):
        try:
            dates = self.db.session.query(func.min(RequestResult.start), func.max(RequestResult.end)).filter_by(
                request_id=request_id).one()
            Request.query.filter_by(id=request_id).update(
                {'status': status, 'start': dates[0], 'end': dates[1]})
            self.db.session.commit()

        except Exception:
            self.logger.exception("Error clossing request with id {}".format(request_id))
            return False

        return True

    def get_request_instrument_list(self, request_id):
        try:
            instrument_list = None
            request = self.db.session.query(Request.instrument_list).filter_by(id=request_id).one_or_none()
            if request is not None:
                instrument_list = json.loads(request[0])
        except Exception:
            self.logger.exception("Error selecting request instrument_list for request_id {}".format(request_id))
            instrument_list = None

        return instrument_list

    def get_num_requests_pending(self, enrolment):
        num_requests = Request.query.filter(Request.is_enrolment == enrolment,
                                            Request.status == TESLA_REQUEST_STATUS.PENDING,
                                            ).count()

        return int(num_requests)

    def get_num_requests_processed(self, enrolment):
        num_requests = Request.query.filter(Request.is_enrolment == enrolment,
                                            Request.status == TESLA_REQUEST_STATUS.DONE,
                                            ).count()

        return int(num_requests)

    def get_num_requests_failed(self, enrolment):
        num_requests = Request.query.filter(Request.is_enrolment == enrolment,
                                            Request.status == TESLA_REQUEST_STATUS.FAILED,
                                            ).count()

        return int(num_requests)

    def create_initial_request_result(self, request_id, instrument_id):
        try:
            req_result = RequestResult(request_id=request_id, instrument_id=instrument_id,
                                       status=0, progress=0.0)
            self.db.session.add(req_result)
            self.db.session.commit()
            self.db.session.refresh(req_result)
        except Exception:
            self.logger.exception("Error creating initial request result for request {} and instrument {}".format(request_id, instrument_id))
            self.db.session.rollback()
            return None

        return req_result

    def create_request_data(self, request_id, data):
        try:
            req_data = RequestData(request_id=request_id, data=data)
            self.db.session.add(req_data)
            self.db.session.commit()
            self.db.session.refresh(req_data)
        except Exception:
            self.logger.exception("Error creating request data for request {}".format(request_id))
            self.db.session.rollback()
            return None

        return req_data

    def update_request_result_status(self, request_id, instrument_id, progress, status):
        try:
            RequestResult.query.filter_by(request_id=request_id, instrument_id=instrument_id)\
                .update({'status': status, 'progress': progress})
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error updating request result status for request {} and instrument{}".format(request_id, instrument_id))
            return False

        return True

    def create_update_request_result_audit_data(self, request_id, instrument_id, with_enrolment, with_request, data):

        try:
            req_audit = self.db.session.query(RequestAudit).filter(RequestAudit.request_id == request_id,
                                                                   RequestAudit.instrument_id == instrument_id).with_for_update().one_or_none()

            if req_audit is None:
                req_audit = RequestAudit(request_id=request_id, instrument_id=instrument_id, enrolment=with_enrolment,
                                         request=with_request, data=data)
                self.db.session.add(req_audit)
            else:
                req_audit.enrolment = with_enrolment
                req_audit.request = with_request
                req_audit.data = data
            self.db.session.commit()
            self.db.session.refresh(req_audit)

        except Exception:
            self.logger.exception("Error creating new request result audit {}".format(req_audit))
            req_audit = None

        return req_audit

    def create_update_result(self, request_id, instrument_id, start, end, error_code, error_message,
                             result, detail, status, progress):
        try:

            req_result = self.db.session.query(RequestResult).filter(RequestResult.request_id==request_id,
                                        RequestResult.instrument_id == instrument_id).with_for_update().one_or_none()

            if req_result is None:
                req_result = RequestResult(request_id=request_id, instrument_id=instrument_id, start=start,
                                               end=end, error_code=error_code, error_message=error_message,
                                               result=result, detail=detail, status=status, progress=progress)
                self.db.session.add(req_result)
            else:
                req_result.start = start
                req_result.end = end
                req_result.error_code = error_code
                req_result.error_message = error_message
                req_result.result = result
                req_result.detail = detail
                req_result.status = status
                req_result.progress = progress
            self.db.session.commit()
            self.db.session.refresh(req_result)
        except Exception:
            self.logger.exception("Error creating new request result {}".format(req_result))
            req_result = None

        return req_result

    def update_request_status(self, request_id, status):
        try:
            Request.query.filter_by(id=request_id).update({'status': status})
            self.db.session.commit()

        except Exception:
            self.logger.exception("Error updating request status for request with id {}".format(request_id))
            return False

        return True

    def update_request_activity(self, request_id, activity_id):
        try:
            Request.query.filter_by(id=request_id).update({'activity_id': activity_id})
            self.db.session.commit()

        except Exception:
            self.logger.exception("Error updating request activity for request with id {}".format(request_id))
            return False

        return True

    def update_enrollment_percentage_from_result(self, request_id, instrument_id, percentage):
        try:
            tesla_id = self.get_request_tesla_id(request_id)
            current_value = self.db.session.query(Enrollment.percentage).filter_by(tesla_id=tesla_id,
                                                                                   instrument_id=instrument_id).scalar()
            if current_value is None:
                status = TESLA_ENROLLMENT_PHASE.ONGOING
                if percentage == 1.0:
                    status = TESLA_ENROLLMENT_PHASE.COMPLETED
                new_enrollment = Enrollment(tesla_id=tesla_id, instrument_id=instrument_id, percentage=percentage, status=status)
                self.db.session.add(new_enrollment)
            else:
                status = TESLA_ENROLLMENT_PHASE.ONGOING
                new_value = max(current_value, percentage)
                if new_value == 1.0:
                    status = TESLA_ENROLLMENT_PHASE.COMPLETED
                Enrollment.query.filter_by(tesla_id=tesla_id, instrument_id=instrument_id).update({'percentage': new_value, 'status': status})
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error updating enrollment percentage from request with id {} for learner {}".format(request_id, tesla_id))
            return False
        return True

    def get_request_tesla_id(self, request_id):
        try:
            request = self.db.session.query(Request.tesla_id).filter_by(id=request_id).one_or_none()
            ret_val = None
            if request is not None:
                ret_val = str(request[0])
        except Exception:
            self.logger.exception("Error selecting request tesla_id for request_id {}".format(request_id))
            ret_val = None

        return ret_val

    def get_request(self, request_id):
        try:
            request = Request.query.filter_by(id=request_id).one_or_none()
        except Exception:
            self.logger.exception("Error selecting request for request_id {}".format(request_id))
            request = None

        return request

    def get_request_data(self, request_id):
        try:
            data = RequestData.query.filter_by(request_id=request_id).one_or_none()
        except Exception:
            self.logger.exception("Error selecting request data for request_id {}".format(request_id))
            data = None

        return data

    def get_request_result_audit(self, request_id, instrument_id):
        try:
            data = RequestAudit.query.filter_by(request_id=request_id, instrument_id=instrument_id).one_or_none()
        except Exception:
            self.logger.exception("Error selecting request result audit data for request_id {} and instrument_id {}".format(request_id, instrument_id))
            data = None

        return data

    def get_request_results_metadata(self, request_id):
        try:
            request_result = RequestResult.query.filter_by(request_id=request_id).all()
        except Exception:
            self.logger.exception("Error selecting request results metadata for request_id {}".format(request_id))
            request_result = None

        return request_result

    def get_request_results_finished_instruments_id(self, request_id):
        try:
            finished_instruments = self.db.session.query(RequestResult.instrument_id).filter(RequestResult.request_id==request_id,
                                                                      RequestResult.status>1).all()
            instruments_list = []
            if finished_instruments is not None:
                instruments_list = [int(x[0]) for x in finished_instruments]
        except Exception:
            self.logger.exception("Error selecting request results finished instruments for request_id {}".format(request_id))
            instruments_list = []

        return instruments_list

    def get_request_results_status_instruments_id(self, request_id, status):
        try:
            instruments = self.db.session.query(RequestResult.instrument_id).filter(RequestResult.request_id==request_id,
                                                                      RequestResult.status==status).all()
            instruments_list = []
            if instruments is not None:
                instruments_list = [int(x[0]) for x in instruments]
        except Exception:
            self.logger.exception("Error selecting request results by status for instruments in request_id {}".format(request_id))
            instruments_list = []

        return instruments_list

    def create_enrollment_request(self, tesla_id, instrument_list, id=None, activity_id=None):
        try:
            enc_list = json.dumps(instrument_list)
            new_request = Request(tesla_id=tesla_id, is_enrolment=True, instrument_list=enc_list, id=id, activity_id=activity_id)
            self.db.session.add(new_request)
            self.db.session.commit()
            self.db.session.refresh(new_request)
        except Exception:
            self.logger.exception("Error creating new enrollment request {}".format(new_request))
            new_request = None

        return new_request

    def create_verification_request(self, tesla_id, activity_id, instrument_list, id=None):
        try:
            enc_list = json.dumps(instrument_list)
            new_request = Request(tesla_id=tesla_id, activity_id=activity_id,
                                  is_enrolment=False, instrument_list=enc_list, id=id)
            self.db.session.add(new_request)
            self.db.session.commit()
            self.db.session.refresh(new_request)
        except Exception:
            self.logger.exception("Error creating new verification request {}".format(new_request))
            new_request = None

        return new_request

    def fix_request_status(self, request_id):
        try:
            request = self.get_request(request_id)

            if request is None:
                return None

            instrument_list = self.get_request_instrument_list(request_id)
            finished_list = self.get_request_results_finished_instruments_id(request_id)

            # Get missing instruments
            missing_instruments = list(set(instrument_list) - set(finished_list))

            # Update request status
            if len(missing_instruments) == 0:
                status = TESLA_REQUEST_STATUS.DONE
                failed = self.get_request_results_status_instruments_id(request_id, TESLA_REQUEST_STATUS.FAILED)
                if len(failed)>0:
                    status = TESLA_REQUEST_STATUS.FAILED
                else:
                    timeout = self.get_request_results_status_instruments_id(request_id, TESLA_REQUEST_STATUS.TIMEOUT)
                    if len(timeout) > 0:
                        status = TESLA_REQUEST_STATUS.TIMEOUT
                self.finish_request(request_id, status)
            else:
                status = TESLA_REQUEST_STATUS.RUNNING
                if len(instrument_list) == len(missing_instruments):
                    status = TESLA_REQUEST_STATUS.PENDING
                self.update_request_status(request_id, status)

        except Exception:
            self.logger.exception("Error creating new verification request {}".format(request_id))
            status = None

        return status

    def fix_enrolment_status(self):
        try:
            Enrollment.query.filter(Enrollment.percentage==1.0).update({'status': TESLA_ENROLLMENT_PHASE.COMPLETED})
            Enrollment.query.filter(Enrollment.percentage<1.0, Enrollment.percentage>0.0).update({'status': TESLA_ENROLLMENT_PHASE.ONGOING})
            Enrollment.query.filter(Enrollment.percentage == 0.0).update({'status': TESLA_ENROLLMENT_PHASE.NOT_STARTED})
        except Exception:
            self.logger.exception("Error fixing enrolment status")

    def fix_request_end_date(self):
        try:
            RequestResult.query.filter(RequestResult.end == '0001-01-01 00:00:00.000000',
                                       RequestResult.status > TESLA_RESULT_STATUS.PENDING,
                                       RequestResult.error_code==0).update({'end': None, 'status': TESLA_RESULT_STATUS.PENDING, 'progress': 0})
            Request.query.filter(RequestResult.request_id == Request.id,
                                 RequestResult.status == TESLA_RESULT_STATUS.PENDING,
                                 Request.status > TESLA_REQUEST_STATUS.PENDING).update({'end': None, 'status': TESLA_REQUEST_STATUS.PENDING})

        except Exception:
            self.logger.exception("Error fixing request finalization date")
