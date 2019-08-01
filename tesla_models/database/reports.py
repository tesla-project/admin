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

from tesla_models.models import Course, Activity, CourseActivity, CourseLearner, Learner, InformedConsent, \
    Request, RequestResult, Enrollment, ActivityInstrument, Instrument
from tesla_models.constants import TESLA_REQUEST_STATUS, TESLA_ENROLLMENT_PHASE, TESLA_RESULT_STATUS
from sqlalchemy import or_, not_, func, funcfilter
from sqlalchemy.sql import label
from flask_sqlalchemy import Pagination
from tesla_models import schemas
import datetime


class ReportsDB(object):

    def __init__(self, db, logger):
        self.logger = logger
        self.db = db

    def get_activity_learners_with_results(self, activity_id, instrument_ids=None, page=1, max_per_page=20):
        results = []
        try:
            query = self.db.session.query(Request.tesla_id).filter(RequestResult.request_id==Request.id, Request.activity_id==activity_id).group_by(Request.tesla_id)

            if instrument_ids is not None:
                query.filter(RequestResult.instrument_id.in_(instrument_ids))

            results = query.group_by(Request.tesla_id).order_by(Request.tesla_id).paginate(page=page, max_per_page=max_per_page)

        except Exception:
            self.logger.exception("Error getting list of activities")
            results = Pagination(None, page, max_per_page, 0, [])

        return results

    def get_activity_instruments_with_requests(self, activity_id, instrument_id=None):
        try:
            if instrument_id is None:
                instruments = Instrument.query.filter(Request.activity_id==activity_id, Request.id==RequestResult.request_id,
                                    RequestResult.instrument_id==Instrument.id).group_by(Instrument.id).order_by(Instrument.id).all()
            else:
                instruments = Instrument.query.filter(Request.activity_id == activity_id,
                                                      Request.id == RequestResult.request_id,
                                                      RequestResult.instrument_id == instrument_id,
                                                      RequestResult.instrument_id == Instrument.id).group_by(
                    Instrument.id).order_by(Instrument.id).all()


        except Exception:
            self.logger.exception("Error getting list of instruments with requests for a certain activity")
            instruments = []

        return list(instruments)

    def _get_contained_course_ids(self, course_id):
        child_courses = [course_id]

        children = Course.query.filter(Course.parent_id==course_id).all()
        for child in children:
            child_courses += self._get_contained_course_ids(child.id)

        return child_courses

    def get_course_learners_with_results(self, course_id, instrument_ids=None, page=1, max_per_page=20):
        results = []
        try:
            related_courses_ids = self._get_contained_course_ids(course_id)

            query = self.db.session.query(Request.tesla_id).filter(
                CourseActivity.course_id.in_(related_courses_ids),
                Request.activity_id == CourseActivity.activity_id,
                RequestResult.request_id==Request.id
                ).group_by(Request.tesla_id)

            if instrument_ids is not None:
                query.filter(RequestResult.instrument_id.in_(instrument_ids))

            results = query.group_by(Request.tesla_id).order_by(Request.tesla_id).paginate(page=page, max_per_page=max_per_page)

        except Exception:
            self.logger.exception("Error getting list of learners with requests for a certain course")
            results = Pagination(None, page, max_per_page, 0, [])

        return results

    def get_course_instruments_with_requests(self, course_id):
        try:
            related_courses_ids = self._get_contained_course_ids(course_id)
            instruments = Instrument.query.filter(CourseActivity.course_id.in_(related_courses_ids),
                                                  Request.activity_id==CourseActivity.activity_id,
                                                  Request.id==RequestResult.request_id,
                                                  RequestResult.instrument_id==Instrument.id
                                                  ).group_by(Instrument.id).order_by(Instrument.id).all()

        except Exception:
            self.logger.exception("Error getting list of instruments with requests for a certain course")
            instruments = []

        return list(instruments)

    def get_activity_learner_temporal_results(self, activity_id, tesla_id, instrument_id):
        try:
            result_points = self.db.session.query(Request.created.label('date'), RequestResult.result.label('value'), RequestResult.error_code.label('error')).filter(
                                                  Request.activity_id==activity_id,
                                                  Request.tesla_id==tesla_id,
                                                  Request.id == RequestResult.request_id,
                                                  RequestResult.instrument_id == instrument_id,
                                                  RequestResult.status==TESLA_RESULT_STATUS.DONE,
                                                  ).order_by(Request.created).all()

        except Exception:
            self.logger.exception("Error getting temporal list of instruments results for a certain activity")
            result_points = []

        return list(result_points)

    def get_course_learner_temporal_results(self, course_id, tesla_id, instrument_id):
        try:
            related_courses_ids = self._get_contained_course_ids(course_id)
            result_points = self.db.session.query(Request.created.label('date'),
                                                  RequestResult.result.label('value'), RequestResult.error_code.label('error')).filter(
                CourseActivity.course_id.in_(related_courses_ids),
                Request.activity_id == CourseActivity.activity_id,
                Request.tesla_id == tesla_id,
                Request.id == RequestResult.request_id,
                RequestResult.instrument_id == instrument_id,
                RequestResult.status == TESLA_RESULT_STATUS.DONE
            ).order_by(Request.created).all()

        except Exception:
            self.logger.exception("Error getting temporal list of instruments results for a certain course")
            result_points = []

        return list(result_points)

    def get_course_learner_temporal_failed_requests(self, course_id, tesla_id):
        try:
            related_courses_ids = self._get_contained_course_ids(course_id)
            result_points = self.db.session.query(Request.created.label('date'),
                                                  RequestResult.result.label('value'), RequestResult.error_code.label('error')).filter(
                CourseActivity.course_id.in_(related_courses_ids),
                Request.activity_id == CourseActivity.activity_id,
                Request.tesla_id == tesla_id,
                Request.id == RequestResult.request_id,
                or_(RequestResult.status == TESLA_RESULT_STATUS.FAILED, RequestResult.status == TESLA_RESULT_STATUS.TIMEOUT)
            ).order_by(Request.created).all()

        except Exception:
            self.logger.exception("Error getting temporal list of failed requests for a certain course")
            result_points = []

        return list(result_points)

    def get_activity_learner_temporal_failed_requests(self, activity_id, tesla_id):
        try:
            result_points = self.db.session.query(Request.created.label('date'),
                                                  RequestResult.result.label('value'), RequestResult.error_code.label('error')).filter(
                Request.activity_id == activity_id,
                Request.tesla_id == tesla_id,
                Request.id == RequestResult.request_id,
                or_(RequestResult.status == TESLA_RESULT_STATUS.FAILED, RequestResult.status == TESLA_RESULT_STATUS.TIMEOUT)
            ).order_by(Request.created).all()

        except Exception:
            self.logger.exception("Error getting temporal list of failed requests for a certain activity")
            result_points = []

        return list(result_points)

    def get_course_learner_temporal_failed_requests(self, course_id, tesla_id):
        try:
            related_courses_ids = self._get_contained_course_ids(course_id)
            result_points = self.db.session.query(Request.created.label('date'),
                                                  RequestResult.result.label('value'), RequestResult.error_code.label('error')).filter(
                CourseActivity.course_id.in_(related_courses_ids),
                Request.activity_id == CourseActivity.activity_id,
                Request.tesla_id == tesla_id,
                Request.id == RequestResult.request_id,
                or_(RequestResult.status == TESLA_RESULT_STATUS.FAILED, RequestResult.status == TESLA_RESULT_STATUS.TIMEOUT)
            ).order_by(Request.created).all()

        except Exception:
            self.logger.exception("Error getting temporal list of failed requests for a certain course")
            result_points = []

        return list(result_points)
