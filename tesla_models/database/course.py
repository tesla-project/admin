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
    ActivityInstrument, Enrollment, Request, RequestResult
from sqlalchemy import asc, desc, or_, func, funcfilter, and_
from sqlalchemy.sql import label
from .utils import encode_data, decode_data
from tesla_models.constants import TESLA_REQUEST_STATUS, TESLA_ENROLLMENT_PHASE, TESLA_RESULT_STATUS
import datetime


class CourseDB(object):

    def __init__(self, db, logger):
        self.logger = logger
        self.db = db

    def create_course(self, code, description, start, end, vle_id=None, vle_course_id=None, parent_id=None):
        try:
            new_course = Course(code=code, description=description, start=start, end=end,
                                vle_id=vle_id, vle_course_id=vle_course_id, parent_id=parent_id)

            self.db.session.add(new_course)
            self.db.session.commit()
            self.db.session.refresh(new_course)
        except Exception:
            self.logger.exception("Error creating new course {}".format(new_course))
            new_activity = None

        return new_course

    def update_course(self, id, code, description, start, end, vle_id=None, vle_course_id=None, parent_id=None):
        try:
            Course.query.filter_by(id=id) \
                .update({'code': code, 'description': description, 'start': start, 'end': end,
                         'vle_id': vle_id, 'vle_course_id': vle_course_id, 'parent_id': parent_id})
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error updating course for id {}".format(id))
            return False

        return True

    def get_course(self, id):
        try:
            course = Course.query.filter_by(id=id).one_or_none()
        except Exception:
            self.logger.exception("Error selecting course for id {}".format(id))
            course = None

        return course

    def get_course_by_code(self, code):
        try:
            course = Course.query.filter_by(code=code).one_or_none()
        except Exception:
            self.logger.exception("Error selecting course for code {}".format(code))
            course = None

        return course

    def get_active_courses(self):
        try:
            current_date = datetime.date.today()
            courses = Course.query.filter(or_(Course.start==None, Course.start<=current_date),
                                          or_(Course.end == None, Course.end>=current_date)).order_by(Course.code).all()
        except Exception:
            self.logger.exception("Error selecting active courses")
            courses = None

        return courses

    def get_active_top_courses(self):
        try:
            current_date = datetime.date.today()
            courses = Course.query.filter(Course.parent_id==None, or_(Course.start==None, Course.start<=current_date),
                                          or_(Course.end == None, Course.end>=current_date)).order_by(Course.code).all()
        except Exception:
            self.logger.exception("Error selecting active top courses")
            courses = None

        return courses


    def get_activities(self, course_id, q=None, limit=None, offset=0, sort='id', order='asc'):
        results = []
        try:
            if sort is '' or sort is None:
                sort = 'id'

            if q is not None and q is not '':
                q = '%'+str(q)+'%'
                query = Activity.query.filter(CourseActivity.course_id == course_id,
                                              Activity.id == CourseActivity.activity_id,
                                              or_(Activity.description.like(q), Activity.activity_type.like(q)))
            else:
                query = Activity.query.filter(CourseActivity.course_id == course_id,
                                              Activity.id == CourseActivity.activity_id)

            if order == 'asc':
                query = query.order_by(asc(sort))
            else:
                query = query.order_by(desc(sort))

            query = query.offset(offset)

            if limit is not None:
                query = query.limit(limit)

            results = query.all()

        except Exception:
            self.logger.exception("Error getting list of activities")

        return results

    def count_activities(self, course_id, q=None, limit=None, offset=0):
        result = 0
        try:
            if q is not None:
                q = '%'+str(q)+'%'
                query = Activity.query.filter(CourseActivity.course_id==course_id,
                                              Activity.id==CourseActivity.activity_id,
                                              or_(Activity.description.like(q), Activity.activity_type.like(q)))
            else:
                query = Activity.query.filter(CourseActivity.course_id == course_id,
                                              Activity.id == CourseActivity.activity_id)

            query = query.offset(offset)

            if limit is not None:
                query = query.limit(limit)

            result = query.count()

        except Exception:
            self.logger.exception("Error getting activities count")

        return result

    def get_available_activities(self, course_id, q=None, limit=None, offset=0, sort='id', order='asc'):
        results = []
        try:
            course_activities = CourseActivity.query.filter(CourseActivity.course_id == course_id).all()
            act_list = [c.activity_id for c in course_activities]
            if sort is '' or sort is None:
                sort = 'id'

            if q is not None and q is not '':
                q = '%'+str(q)+'%'
                query = Activity.query.filter(Activity.id.notin_(act_list),
                                              or_(Activity.description.like(q), Activity.activity_type.like(q)))
            else:
                query = Activity.query.filter(Activity.id.notin_(act_list))

            if order == 'asc':
                query = query.order_by(asc(sort))
            else:
                query = query.order_by(desc(sort))

            query = query.offset(offset)

            if limit is not None:
                query = query.limit(limit)

            results = query.all()

        except Exception:
            self.logger.exception("Error getting list of available activities")

        return results

    def count_available_activities(self, course_id, q=None, limit=None, offset=0):
        result = 0
        try:
            course_activities = CourseActivity.query.filter(CourseActivity.course_id==course_id).all()
            act_list = [c.activity_id for c in course_activities]
            if q is not None:
                q = '%'+str(q)+'%'
                query = Activity.query.filter(Activity.id.notin_(act_list),
                                              or_(Activity.description.like(q), Activity.activity_type.like(q)))
            else:
                query = Activity.query.filter(Activity.id.notin_(act_list))

            query = query.offset(offset)

            if limit is not None:
                query = query.limit(limit)

            result = query.count()

        except Exception:
            self.logger.exception("Error getting available activities count")

        return result

    def delete_activity(self, course_id, activity_id):
        try:
            self.db.session.query(CourseActivity).filter(CourseActivity.course_id==course_id,
                                        CourseActivity.activity_id==activity_id).delete()
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error removing activity {} from course {}".format(activity_id, course_id))
            self.db.session.rollback()
            return False

        return True

    def add_activity(self, course_id, activity_id):
        try:
            # Check if the activity is already assigned
            new_course_activity = CourseActivity.query.filter(CourseActivity.course_id==course_id,
                                        CourseActivity.activity_id==activity_id).one_or_none()
            if new_course_activity is None:
                new_course_activity = CourseActivity(course_id=course_id, activity_id=activity_id)
                self.db.session.add(new_course_activity)
                self.db.session.commit()
                self.db.session.refresh(new_course_activity)
        except Exception:
            self.logger.exception("Error adding activity {} to course {}".format(activity_id, course_id))
            new_course_activity = None

        return new_course_activity

    def delete_learner(self, course_id, tesla_id):
        try:
            self.db.session.query(CourseLearner).filter(CourseLearner.course_id == course_id,
                                       CourseLearner.tesla_id == tesla_id).delete()
            self.db.session.commit()

        except Exception:
            self.logger.exception("Error removing learner {} from course {}".format(tesla_id, course_id))
            self.db.session.rollback()
            return False

        return True

    def add_learner(self, course_id, tesla_id):
        try:
            # Check if the learner is already assigned
            new_course_learner = CourseLearner.query.filter(CourseLearner.course_id==course_id,
                                                            CourseLearner.tesla_id==tesla_id).one_or_none()
            if new_course_learner is None:
                new_course_learner = CourseLearner(course_id=course_id, tesla_id=tesla_id)
                self.db.session.add(new_course_learner)
                self.db.session.commit()
                self.db.session.refresh(new_course_learner)
        except Exception:
            self.logger.exception("Error adding learner {} to course {}".format(tesla_id, course_id))
            new_course_learner = None

        return new_course_learner

    def delete_activities(self, course_id):
        try:
            self.db.session.query(CourseActivity).filter(CourseActivity.course_id==course_id).delete()
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error removing activities from course {}".format(course_id))
            self.db.session.rollback()
            return False

        return True

    def delete_learners(self, course_id):
        try:
            self.db.session.query(CourseLearner).filter(CourseLearner.course_id==course_id).delete()
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error removing learners from course {}".format(course_id))
            self.db.session.rollback()
            return False

        return True

    def delete_course(self, course_id):
        try:
            self.db.session.query(CourseActivity).filter(CourseActivity.course_id == course_id).delete()
            self.db.session.query(CourseLearner).filter(CourseLearner.course_id == course_id).delete()
            self.db.session.query(Course).filter(Course.id == course_id).delete()
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error removing course {}".format(course_id))
            self.db.session.rollback()
            return False

        return True



    def num_learners(self, course_id):
        num_learners = 0
        try:
            num_learners = CourseLearner.query.filter(CourseLearner.course_id == course_id).count()
        except Exception:
            self.logger.exception("Error counting course learners {}".format(course_id))

        return int(num_learners)

    def num_activities(self, course_id):
        num_activities = 0
        try:
            num_activities = CourseActivity.query.filter(CourseActivity.course_id == course_id).count()
        except Exception:
            self.logger.exception("Error getting course activities")

        return int(num_activities)

    def instruments(self, course_id):
        instrument_list = []
        try:
            configured_instruments = ActivityInstrument.query.filter(ActivityInstrument.activity_id==CourseActivity.activity_id, CourseActivity.course_id==course_id).all()
            for inst_conf in configured_instruments:
                instrument_list.append(inst_conf.instrument_id)
                if inst_conf.alternative_instrument_id is not None:
                    instrument_list.append(inst_conf.alternative_instrument_id)

            instrument_list = list(set(instrument_list))

        except:
            self.logger.exception("Error getting course instruments")
        return instrument_list

    def num_learners_enrolment_complete(self, course_id, instrument_id):
        try:
            num_learners = CourseLearner.query.filter(CourseLearner.course_id==course_id,
                                                      Enrollment.tesla_id==CourseLearner.tesla_id,
                                                      Enrollment.instrument_id==instrument_id,
                                                      Enrollment.status==TESLA_ENROLLMENT_PHASE.COMPLETED).count()
        except:
            self.logger.exception("Error getting learners with completed enrolment for a course")
            num_learners = 0
        return int(num_learners)

    def num_learners_enrolment_started(self, course_id, instrument_id):
        try:
            num_learners = CourseLearner.query.filter(CourseLearner.course_id==course_id,
                                                      Enrollment.tesla_id==CourseLearner.tesla_id,
                                                      Enrollment.instrument_id==instrument_id,
                                                      Enrollment.status==TESLA_ENROLLMENT_PHASE.ONGOING).count()
        except:
            self.logger.exception("Error getting learners with started enrolment for a course")
            num_learners = 0
        return int(num_learners)

    def num_enrolment_requests(self, course_id, instrument_id):
        return -1

    def num_verification_requests(self, course_id, instrument_id):
        try:
            num_requests = Request.query.filter(Request.activity_id==CourseActivity.activity_id,
                                                Request.is_enrolment == False,
                                                CourseActivity.course_id==course_id,
                                                Request.instrument_list.like('%{}%'.format(instrument_id))
                                                ).count()
        except:
            self.logger.exception("Error getting number of validation requests")
            num_requests = 0
        return int(num_requests)

    def num_learners_with_enrolment_requests(self, course_id, instrument_id):
        return -1

    def num_learners_with_verification_requests(self, course_id, instrument_id):
        try:
            num_learners = self.db.session.query(Request.tesla_id, label('num_requests', func.count(Request.id))) \
                .filter(Request.activity_id==CourseActivity.activity_id,
                        Request.is_enrolment == False,
                        CourseActivity.course_id == course_id,
                        RequestResult.request_id == Request.id,
                        RequestResult.instrument_id == instrument_id) \
                .group_by(Request.tesla_id).count()
        except:
            self.logger.exception("Error getting users with validation requests")
            num_learners = 0
        return int(num_learners)

    def verification_results(self, course_id, instrument_id):
        try:
            results = self.db.session.query(RequestResult.result) \
                .filter(Request.activity_id==CourseActivity.activity_id,
                        Request.is_enrolment == False,
                        CourseActivity.course_id == course_id,
                        RequestResult.request_id == Request.id,
                        RequestResult.instrument_id == instrument_id,
                        RequestResult.status == TESLA_RESULT_STATUS.DONE) \
                .all()
        except:
            self.logger.exception("Error getting users with validation requests")
            return []
        return [float(r.result) for r in results]

    def _get_contained_course_ids(self, course_id):
        child_courses = [course_id]

        children = Course.query.filter(Course.parent_id==course_id).all()
        for child in children:
            child_courses += self._get_contained_course_ids(child.id)

        return child_courses

    def get_child_courses_with_synch_data(self, course_id):
        try:
            related_courses = self._get_contained_course_ids(course_id)
            courses = Course.query.filter(Course.id.in_(related_courses), Course.vle_id!=None, Course.vle_course_id!=None).all()
        except:
            self.logger.exception("Error getting users with validation requests")
            return []
        return list(courses)

    def get_course_learner_summary(self, course_id, tesla_id):

        try:
            related_courses = self._get_contained_course_ids(course_id)
            summary = self.db.session.query(
                RequestResult.instrument_id,
                func.max(Enrollment.percentage).label('enrolment_percentage'),
                funcfilter(func.count(1), RequestResult.status==TESLA_RESULT_STATUS.DONE).label('valid'),
                funcfilter(func.count(1), RequestResult.status == TESLA_RESULT_STATUS.PENDING).label('pending'),
                funcfilter(func.count(1), or_(RequestResult.status == TESLA_RESULT_STATUS.TIMEOUT,
                                              RequestResult.status== TESLA_RESULT_STATUS.FAILED)).label('failed'),
                funcfilter(func.min(RequestResult.result), RequestResult.status==TESLA_RESULT_STATUS.DONE).label('min'),
                funcfilter(func.max(RequestResult.result), RequestResult.status == TESLA_RESULT_STATUS.DONE).label('max'),
                funcfilter(func.avg(RequestResult.result), RequestResult.status == TESLA_RESULT_STATUS.DONE).label('average')
            ).filter(
                Request.tesla_id == tesla_id,
                CourseActivity.activity_id==Request.activity_id,
                CourseActivity.course_id.in_(related_courses),
                RequestResult.request_id == Request.id
            ).outerjoin(Enrollment,
                        and_(Enrollment.tesla_id==tesla_id,
                            Enrollment.instrument_id==RequestResult.instrument_id)
            ).group_by(
                RequestResult.instrument_id
            ).all()
        except Exception:
            self.logger.exception("Error getting summary for a learner and course")
            summary = None

        return summary

    def get_course_summary(self, course_id):

        try:
            related_courses = self._get_contained_course_ids(course_id)
            summary = self.db.session.query(
                RequestResult.instrument_id,
                func.avg(Enrollment.percentage).label('enrolment_percentage'),
                funcfilter(func.count(1), RequestResult.status==TESLA_RESULT_STATUS.DONE).label('valid'),
                funcfilter(func.count(1), RequestResult.status == TESLA_RESULT_STATUS.PENDING).label('pending'),
                funcfilter(func.count(1), or_(RequestResult.status == TESLA_RESULT_STATUS.TIMEOUT,
                                              RequestResult.status== TESLA_RESULT_STATUS.FAILED)).label('failed'),
                funcfilter(func.min(RequestResult.result), RequestResult.status==TESLA_RESULT_STATUS.DONE).label('min'),
                funcfilter(func.max(RequestResult.result), RequestResult.status == TESLA_RESULT_STATUS.DONE).label('max'),
                funcfilter(func.avg(RequestResult.result), RequestResult.status == TESLA_RESULT_STATUS.DONE).label('average')
            ).filter(
                CourseActivity.activity_id==Request.activity_id,
                CourseActivity.course_id.in_(related_courses),
                RequestResult.request_id == Request.id
            ).outerjoin(Enrollment,
                            Enrollment.instrument_id==RequestResult.instrument_id
            ).group_by(
                RequestResult.instrument_id
            ).all()
        except Exception:
            self.logger.exception("Error getting summary for a course")
            summary = None

        return summary
