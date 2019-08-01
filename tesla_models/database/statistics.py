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

from tesla_models.models import Course, Activity, CourseActivity, CourseLearner, Learner, InformedConsent, Request, RequestResult, Enrollment, ActivityInstrument
from tesla_models.constants import TESLA_REQUEST_STATUS, TESLA_ENROLLMENT_PHASE, TESLA_RESULT_STATUS
from sqlalchemy import or_, not_, func, funcfilter
from sqlalchemy.sql import label
from tesla_models import schemas
import datetime


class StatisticsDB(object):

    def __init__(self, db, logger):
        self.logger = logger
        self.db = db

    def _get_current_informed_consent_version(self):
        version = None
        try:
            ic = InformedConsent.query.filter(
                InformedConsent.valid_from<=datetime.datetime.now()
            ).order_by(InformedConsent.version.desc()).limit(1).one_or_none()
        except Exception:
            self.logger.exception("Error selecting current informed consent version")
            ic = None

        if ic is not None:
            version = ic.version

        return version

    def _get_active_courses(self):
        try:
            current_date = datetime.date.today()
            courses = Course.query.filter(or_(Course.start==None, Course.start<=current_date),
                                          or_(Course.end == None, Course.end>=current_date)).all()
        except Exception:
            self.logger.exception("Error selecting active courses")
            courses = None

        return courses

    def _get_active_top_courses(self):
        try:
            current_date = datetime.date.today()
            courses = Course.query.filter(Course.parent_id==None, or_(Course.start==None, Course.start<=current_date),
                                          or_(Course.end == None, Course.end>=current_date)).all()
        except Exception:
            self.logger.exception("Error selecting active courses")
            courses = None

        return courses

    def _get_active_courses_total_learners(self):
        try:
            course_learners = self.db.session.query(CourseLearner.course_id, Course.description, func.count()).filter(
                CourseLearner.course_id == Course.id,
                or_(Course.start == None, Course.start<=datetime.datetime.now()),
                or_(Course.end == None, Course.end >= datetime.datetime.now())
            ).group_by(CourseLearner.course_id, Course.description).all()

        except Exception:
            self.logger.exception("Error getting list of total learners for active courses")

        return course_learners

    def _get_active_courses_learners_with_valid_ic(self, version):
        try:
            if version is None:
                version = '0.0.0'
            version = '.'.join(version.split('.')[0:2])
            course_learners = self.db.session.query(
                CourseLearner.course_id, Course.description, func.count()
            ).outerjoin(Learner, InformedConsent, aliased=True).filter(
                CourseLearner.course_id == Course.id,
                or_(Course.start == None, Course.start <= datetime.datetime.now()),
                or_(Course.end == None, Course.end >= datetime.datetime.now()),
                CourseLearner.tesla_id == Learner.tesla_id,
                Learner.consent_id != None,
                Learner.consent_id == InformedConsent.id,
                Learner.consent_rejected == None,
                InformedConsent.version.like(version + '.%')
            ).group_by(CourseLearner.course_id, Course.description).all()
        except Exception:
            self.logger.exception("Error getting list of num learners with valid Informed Consent for active courses")

        return course_learners

    def _get_active_courses_learners_with_outdated_ic(self, version):
        try:
            if version is None:
                version = '0.0.0'
            version = '.'.join(version.split('.')[0:2])
            course_learners = self.db.session.query(
                CourseLearner.course_id, Course.description, func.count()
            ).outerjoin(Learner, InformedConsent, aliased=True).filter(
                CourseLearner.course_id == Course.id,
                or_(Course.start == None, Course.start <= datetime.datetime.now()),
                or_(Course.end == None, Course.end >= datetime.datetime.now()),
                CourseLearner.tesla_id == Learner.tesla_id,
                Learner.consent_id != None,
                Learner.consent_id == InformedConsent.id,
                Learner.consent_rejected == None,
                not_(InformedConsent.version.like(version + '.%'))
            ).group_by(CourseLearner.course_id, Course.description).all()
        except Exception:
            self.logger.exception("Error getting list of num learners with valid Informed Consent for active courses")

        return course_learners

    def _get_active_courses_learners_with_rejected_ic(self):
        try:
            course_learners = self.db.session.query(
                CourseLearner.course_id, Course.description, func.count()
            ).outerjoin(Learner, InformedConsent, aliased=True).filter(
                CourseLearner.course_id == Course.id,
                or_(Course.start == None, Course.start <= datetime.datetime.now()),
                or_(Course.end == None, Course.end >= datetime.datetime.now()),
                CourseLearner.tesla_id == Learner.tesla_id,
                Learner.consent_id != None,
                Learner.consent_rejected != None
            ).group_by(CourseLearner.course_id, Course.description).all()
        except Exception:
            self.logger.exception("Error getting list of num learners with valid Informed Consent for active courses")

        return course_learners

    def _get_active_courses_learners_with_no_ic(self):
        try:
            course_learners = self.db.session.query(
                CourseLearner.course_id, Course.description, func.count()
            ).outerjoin(Learner, InformedConsent, aliased=True).filter(
                CourseLearner.course_id == Course.id,
                or_(Course.start == None, Course.start <= datetime.datetime.now()),
                or_(Course.end == None, Course.end >= datetime.datetime.now()),
                CourseLearner.tesla_id == Learner.tesla_id,
                Learner.consent_id == None
            ).group_by(CourseLearner.course_id, Course.description).all()
        except Exception:
            self.logger.exception("Error getting list of num learners with valid Informed Consent for active courses")

        return course_learners

    def get_active_course_learner_statistics(self):
        total = self._get_active_courses_total_learners()
        current_version = self._get_current_informed_consent_version()
        valid_ic = self._get_active_courses_learners_with_valid_ic(current_version)
        outdated_ic = self._get_active_courses_learners_with_outdated_ic(current_version)
        rejected_ic = self._get_active_courses_learners_with_rejected_ic()
        no_ic = self._get_active_courses_learners_with_no_ic()

        # Initialize the statistics object
        learner_stats = {}
        active_courses = self._get_active_courses()
        for c in active_courses:
            learner_stats[c.id] = {'id': c.id, 'code': c.code, 'description': c.description, 'start': c.start,
                                   'end': c.end,
                                   'total': 0, 'no_ic': 0, 'valid_ic': 0, 'rejected_ic': 0, 'outdated_ic': 0}
        for c in total:
            if c.course_id in learner_stats:
                learner_stats[c.course_id]['total'] = c[2]
        for c in valid_ic:
            if c.course_id in learner_stats:
                learner_stats[c.course_id]['valid_ic'] = c[2]
        for c in outdated_ic:
            if c.course_id in learner_stats:
                learner_stats[c.course_id]['outdated_ic'] = c[2]
        for c in rejected_ic:
            if c.course_id in learner_stats:
                learner_stats[c.course_id]['rejected_ic'] = c[2]
        for c in no_ic:
            if c.course_id in learner_stats:
                learner_stats[c.course_id]['no_ic'] = c[2]

        return learner_stats

    def _get_contained_course_ids(self, course_id):
        child_courses = [course_id]

        children = Course.query.filter(Course.parent_id==course_id).all()
        for child in children:
            child_courses += self._get_contained_course_ids(child.id)

        return child_courses

    def get_active_top_course_learner_statistics(self, paginate=None):
        current_version = self._get_current_informed_consent_version()
        
        version_parts = current_version.split('.')
        current_version = '{}.{}.'.format(version_parts[0],version_parts[1])

        try:
            current_date = datetime.date.today()
            query = Course.query.filter(Course.parent_id==None, or_(Course.start==None, Course.start<=current_date),
                                          or_(Course.end == None, Course.end>=current_date))

            if paginate is None:
                active_courses = query.paginate()
            else:
                active_courses = paginate.get_results(query)

            learner_stats = schemas.CourseLearnersStatsPagination().dump(active_courses).data
            for c in learner_stats['items']:
                related_course_ids = self._get_contained_course_ids(c['id'])
                course_learner_stats = self.db.session.query(funcfilter(func.count(1), Learner.consent_rejected!=None).label('rejected_ic'),
                      funcfilter(func.count(1), Learner.consent_rejected==None, Learner.consent_accepted==None).label('no_ic'),
                      funcfilter(func.count(1), Learner.consent_rejected==None, InformedConsent.version.like('{}%'.format(current_version))).label('valid_ic'),
                      funcfilter(func.count(1), Learner.consent_rejected==None, InformedConsent.version.notlike('{}%'.format(current_version))).label('outdated_ic'),
                      func.count(1).label('total')
                      ).filter(
                    CourseLearner.course_id.in_(related_course_ids),
                    Learner.tesla_id==CourseLearner.tesla_id).outerjoin(InformedConsent).one_or_none()

                c['total'] = course_learner_stats.total
                c['no_ic'] = course_learner_stats.no_ic
                c['valid_ic'] = course_learner_stats.valid_ic
                c['rejected_ic'] = course_learner_stats.rejected_ic
                c['outdated_ic'] = course_learner_stats.outdated_ic

        except Exception:
            self.logger.exception("Error selecting active top courses learner statistics")
            learner_stats = None

        return learner_stats

    def num_course_learners_with_verification_requests(self, course_id, instrument_id):
        try:
            related_course_ids = self._get_contained_course_ids(course_id)
            num_learners = self.db.session.query(Request.tesla_id, label('num_requests', func.count(Request.id))) \
                .filter(Request.activity_id==CourseActivity.activity_id,
                        Request.is_enrolment == False,
                        CourseActivity.course_id.in_(related_course_ids),
                        RequestResult.request_id == Request.id,
                        RequestResult.instrument_id == instrument_id) \
                .group_by(Request.tesla_id).count()
        except:
            self.logger.exception("Error getting users with validation requests")
            num_learners = 0
        return int(num_learners)

    def num_activity_learners_with_verification_requests(self, activity_id, instrument_id):
        try:
            num_learners = self.db.session.query(Request.tesla_id, label('num_requests', func.count(Request.id))) \
                .filter(Request.activity_id==activity_id,
                        Request.activity_id==CourseActivity.activity_id,
                        Request.is_enrolment == False,
                        RequestResult.request_id == Request.id,
                        RequestResult.instrument_id == instrument_id) \
                .group_by(Request.tesla_id).count()
        except:
            self.logger.exception("Error getting users with validation requests for an activity")
            num_learners = 0
        return int(num_learners)

    def get_learner_instrument_valid_results_histogram(self, tesla_id, instrument_id):
        try:
            results = self.db.session.query(funcfilter(func.count(1), RequestResult.result>=0, RequestResult.result<0.1).label('<10'),
                      funcfilter(func.count(1), RequestResult.result>=0.1, RequestResult.result<0.2).label('<20'),
                      funcfilter(func.count(1), RequestResult.result>=0.2, RequestResult.result<0.3).label('<30'),
                      funcfilter(func.count(1), RequestResult.result>=0.3, RequestResult.result<0.4).label('<40'),
                      funcfilter(func.count(1), RequestResult.result>=0.4, RequestResult.result<0.5).label('<50'),
                      funcfilter(func.count(1), RequestResult.result>=0.5, RequestResult.result<0.6).label('<60'),
                      funcfilter(func.count(1), RequestResult.result>=0.6, RequestResult.result<0.7).label('<70'),
                      funcfilter(func.count(1), RequestResult.result>=0.7, RequestResult.result<0.8).label('<80'),
                      funcfilter(func.count(1), RequestResult.result>=0.8, RequestResult.result<0.9).label('<90'),
                      funcfilter(func.count(1), RequestResult.result>=0.9, RequestResult.result<=1.0).label('100')
                      ) \
                .filter(Request.is_enrolment == False,
                        Request.tesla_id == tesla_id,
                        RequestResult.request_id == Request.id,
                        RequestResult.instrument_id == instrument_id,
                        RequestResult.status == TESLA_RESULT_STATUS.DONE) \
                .one()
        except:
            self.logger.exception("Error getting learner results histogram")
            return []
        return list(results)

    def verification_course_results_histogram(self, course_id, instrument_id):
        try:
            related_course_ids = self._get_contained_course_ids(course_id)
            results = self.db.session.query(funcfilter(func.count(1), RequestResult.result>=0, RequestResult.result<0.1).label('<10'),
                      funcfilter(func.count(1), RequestResult.result>=0.1, RequestResult.result<0.2).label('<20'),
                      funcfilter(func.count(1), RequestResult.result>=0.2, RequestResult.result<0.3).label('<30'),
                      funcfilter(func.count(1), RequestResult.result>=0.3, RequestResult.result<0.4).label('<40'),
                      funcfilter(func.count(1), RequestResult.result>=0.4, RequestResult.result<0.5).label('<50'),
                      funcfilter(func.count(1), RequestResult.result>=0.5, RequestResult.result<0.6).label('<60'),
                      funcfilter(func.count(1), RequestResult.result>=0.6, RequestResult.result<0.7).label('<70'),
                      funcfilter(func.count(1), RequestResult.result>=0.7, RequestResult.result<0.8).label('<80'),
                      funcfilter(func.count(1), RequestResult.result>=0.8, RequestResult.result<0.9).label('<90'),
                      funcfilter(func.count(1), RequestResult.result>=0.9, RequestResult.result<=1.0).label('100')
                      ) \
                .filter(Request.activity_id==CourseActivity.activity_id,
                        Request.is_enrolment == False,
                        CourseActivity.course_id.in_(related_course_ids),
                        RequestResult.request_id == Request.id,
                        RequestResult.instrument_id == instrument_id,
                        RequestResult.status == TESLA_RESULT_STATUS.DONE) \
                .one()
        except:
            self.logger.exception("Error getting users with validation requests")
            return []
        return list(results)

    def verification_activity_results_histogram(self, activity_id, instrument_id):
        try:
            results = self.db.session.query(funcfilter(func.count(1), RequestResult.result>=0, RequestResult.result<0.1).label('<10'),
                      funcfilter(func.count(1), RequestResult.result>=0.1, RequestResult.result<0.2).label('<20'),
                      funcfilter(func.count(1), RequestResult.result>=0.2, RequestResult.result<0.3).label('<30'),
                      funcfilter(func.count(1), RequestResult.result>=0.3, RequestResult.result<0.4).label('<40'),
                      funcfilter(func.count(1), RequestResult.result>=0.4, RequestResult.result<0.5).label('<50'),
                      funcfilter(func.count(1), RequestResult.result>=0.5, RequestResult.result<0.6).label('<60'),
                      funcfilter(func.count(1), RequestResult.result>=0.6, RequestResult.result<0.7).label('<70'),
                      funcfilter(func.count(1), RequestResult.result>=0.7, RequestResult.result<0.8).label('<80'),
                      funcfilter(func.count(1), RequestResult.result>=0.8, RequestResult.result<0.9).label('<90'),
                      funcfilter(func.count(1), RequestResult.result>=0.9, RequestResult.result<=1.0).label('100')
                      ) \
                .filter(Request.activity_id==activity_id,
                        Request.activity_id==CourseActivity.activity_id,
                        Request.is_enrolment == False,
                        RequestResult.request_id == Request.id,
                        RequestResult.instrument_id == instrument_id,
                        RequestResult.status == TESLA_RESULT_STATUS.DONE) \
                .one()
        except:
            self.logger.exception("Error getting users with validation requests for an activity")
            return []
        return list(results)

    def num_course_learners_enrolment_complete(self, course_id, instrument_id):
        try:
            related_course_ids = self._get_contained_course_ids(course_id)
            num_learners = Learner.query.filter(CourseLearner.course_id.in_(related_course_ids),
                     Learner.tesla_id==CourseLearner.tesla_id,
                     Enrollment.tesla_id==CourseLearner.tesla_id,
                     Enrollment.instrument_id==instrument_id,
                     Enrollment.status==TESLA_ENROLLMENT_PHASE.COMPLETED).group_by(Learner.tesla_id).count()
        except:
            self.logger.exception("Error getting learners with completed enrolment for a course")
            num_learners = 0
        return int(num_learners)

    def num_activity_learners_enrolment_complete(self, activity_id, instrument_id):
        try:
            num_learners = Learner.query.filter(CourseActivity.activity_id==activity_id,
                              CourseActivity.course_id==CourseLearner.course_id,
                              Learner.tesla_id==CourseLearner.tesla_id,
                              Enrollment.tesla_id==CourseLearner.tesla_id,
                              Enrollment.instrument_id==instrument_id,
                              Enrollment.status==TESLA_ENROLLMENT_PHASE.COMPLETED).group_by(Learner.tesla_id).count()
        except:
            self.logger.exception("Error getting learners with completed enrolment for an activity")
            num_learners = 0
        return int(num_learners)

    def num_course_learners_enrolment_started(self, course_id, instrument_id):
        try:
            related_course_ids = self._get_contained_course_ids(course_id)
            num_learners = Learner.query.filter(CourseLearner.course_id.in_(related_course_ids),
                                                Learner.tesla_id==CourseLearner.tesla_id,
                                                Enrollment.tesla_id==CourseLearner.tesla_id,
                                                Enrollment.instrument_id==instrument_id,
                                                Enrollment.status==TESLA_ENROLLMENT_PHASE.ONGOING).group_by(Learner.tesla_id).count()
        except:
            self.logger.exception("Error getting learners with started enrolment for a course")
            num_learners = 0
        return int(num_learners)

    def num_activity_learners_enrolment_started(self, activity_id, instrument_id):
        try:
            num_learners = Learner.query.filter(CourseActivity.activity_id==activity_id,
                                                CourseActivity.course_id==CourseLearner.course_id,
                                                Learner.tesla_id==CourseLearner.tesla_id,
                                                Enrollment.tesla_id==CourseLearner.tesla_id,
                                                Enrollment.instrument_id==instrument_id,
                                                Enrollment.status==TESLA_ENROLLMENT_PHASE.ONGOING).group_by(Learner.tesla_id).count()
        except:
            self.logger.exception("Error getting learners with started enrolment for an activity")
            num_learners = 0
        return int(num_learners)

    def num_learners_course(self, course_id):
        num_learners = 0
        try:
            related_course_ids = self._get_contained_course_ids(course_id)
            num_learners = Learner.query.filter(CourseLearner.course_id.in_(related_course_ids),
                                                CourseLearner.tesla_id==Learner.tesla_id).group_by(Learner.tesla_id).count()
        except Exception:
            self.logger.exception("Error counting course learners {}".format(course_id))

        return int(num_learners)

    def num_learners_activity(self, activity_id):
        num_learners = 0
        try:
            num_learners = Learner.query.filter(CourseActivity.activity_id==activity_id,
                                                CourseLearner.course_id==CourseActivity.course_id,
                                                CourseLearner.tesla_id==Learner.tesla_id,
                                                ).group_by(Learner.tesla_id).count()
        except Exception:
            self.logger.exception("Error counting activity learners {}".format(activity_id))

        return int(num_learners)

    def num_activities_course(self, course_id):
        num_activities = 0
        try:
            related_course_ids = self._get_contained_course_ids(course_id)
            num_activities = Activity.query.filter(CourseActivity.course_id.in_(related_course_ids),
                                                   Activity.id==CourseActivity.activity_id).group_by(Activity.id).count()
        except Exception:
            self.logger.exception("Error getting course activities")

        return int(num_activities)

    def instruments_course(self, course_id):
        instrument_list = []
        try:
            related_course_ids = self._get_contained_course_ids(course_id)
            configured_instruments = ActivityInstrument.query.filter(ActivityInstrument.activity_id==CourseActivity.activity_id, CourseActivity.course_id.in_(related_course_ids)).all()
            for inst_conf in configured_instruments:
                instrument_list.append(inst_conf.instrument_id)
                if inst_conf.alternative_instrument_id is not None:
                    instrument_list.append(inst_conf.alternative_instrument_id)

            instrument_list = list(set(instrument_list))

        except:
            self.logger.exception("Error getting course instruments")
        return instrument_list

    def instruments_activity(self, activity_id):
        instrument_list = []
        try:
            configured_instruments = ActivityInstrument.query.filter(ActivityInstrument.activity_id==activity_id).all()
            for inst_conf in configured_instruments:
                instrument_list.append(inst_conf.instrument_id)
                if inst_conf.alternative_instrument_id is not None:
                    instrument_list.append(inst_conf.alternative_instrument_id)

            instrument_list = list(set(instrument_list))

        except:
            self.logger.exception("Error getting activity instruments")
        return instrument_list

    def get_course_learner_statistics(self, course_id):
        try:
            current_version = self._get_current_informed_consent_version()

            version_parts = current_version.split('.')
            current_version = '{}.{}.'.format(version_parts[0], version_parts[1])

            related_course_ids = self._get_contained_course_ids(course_id)

            course_learner_stats = self.db.session.query(
                    funcfilter(func.count(1), Learner.consent_rejected != None).label('rejected_ic'),
                    funcfilter(func.count(1), Learner.consent_rejected == None, Learner.consent_accepted == None).label(
                        'no_ic'),
                    funcfilter(func.count(1), Learner.consent_rejected == None,
                               InformedConsent.version.like('{}%'.format(current_version))).label('valid_ic'),
                    funcfilter(func.count(1), Learner.consent_rejected == None,
                               InformedConsent.version.notlike('{}%'.format(current_version))).label('outdated_ic'),
                    func.count(1).label('total')
                    ).filter(
                    CourseLearner.course_id.in_(related_course_ids),
                    Learner.tesla_id == CourseLearner.tesla_id).outerjoin(InformedConsent).one_or_none()

        except Exception:
            self.logger.exception("Error geting course learners statistics for course with ID {}".format(course_id))
            course_learner_stats = None

        return course_learner_stats

    def get_activity_learner_statistics(self, activity_id):
        try:
            current_version = self._get_current_informed_consent_version()

            version_parts = current_version.split('.')
            current_version = '{}.{}.'.format(version_parts[0], version_parts[1])

            activity_learner_stats = self.db.session.query(
                    funcfilter(func.count(1), Learner.consent_rejected != None).label('rejected_ic'),
                    funcfilter(func.count(1), Learner.consent_rejected == None, Learner.consent_accepted == None).label(
                        'no_ic'),
                    funcfilter(func.count(1), Learner.consent_rejected == None,
                               InformedConsent.version.like('{}%'.format(current_version))).label('valid_ic'),
                    funcfilter(func.count(1), Learner.consent_rejected == None,
                               InformedConsent.version.notlike('{}%'.format(current_version))).label('outdated_ic'),
                    func.count(1).label('total')
                    ).filter(
                        CourseActivity.activity_id == activity_id,
                        CourseLearner.course_id==CourseActivity.course_id,
                        Learner.tesla_id == CourseLearner.tesla_id).group_by(Learner.tesla_id).outerjoin(InformedConsent).one_or_none()

        except Exception:
            self.logger.exception("Error geting activity learners statistics for activity with ID {}".format(activity_id))
            activity_learner_stats = None

        return activity_learner_stats




