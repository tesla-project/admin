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

from tesla_models.models import Learner, SENDCategory, LearnerSEND, InformedConsent, Request, RequestData, \
    Enrollment, EnrollmentModel, RequestAudit, RequestResult, CourseLearner, Course, Activity, Instrument, ActivityInstrument
from .utils import encode_data, decode_data
from tesla_models.constants import TESLA_REQUEST_STATUS, TESLA_RESULT_STATUS
import datetime
from sqlalchemy import or_


class LearnerDB(object):

    def __init__(self, db, logger):
        self.logger = logger
        self.db = db

    def create_learner(self, tesla_id, crypto_data = None, consent_id=None, consent_accepted=None, consent_rejected=None):
        try:
            new_learner = Learner(tesla_id=tesla_id, crypto_data=crypto_data, consent_id=consent_id,
                                  consent_accepted=consent_accepted, consent_rejected=consent_rejected)

            self.db.session.add(new_learner)
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error creating new learner {}".format(new_learner))
            new_learner = None

        return new_learner

    def update_learner(self, tesla_id, crypto_data = None, consent_id=None, consent_accepted=None, consent_rejected=None):
        try:
            Learner.query.filter_by(tesla_id=tesla_id).update({
                'crypto_data': crypto_data,
                'consent_id': consent_id,
                'consent_accepted': consent_accepted,
                'consent_rejected': consent_rejected
            })
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error updating learner {}".format(tesla_id))
            return False

        return True

    def get_send_categories(self):
        try:
            categories = SENDCategory.query.all()
        except Exception:
            self.logger.exception("Error selecting SEND categories")
            categories = None

        return categories

    def get_send_category(self, id):
        try:
            category = SENDCategory.query.filter(SENDCategory.id == id).one_or_none()
        except Exception:
            self.logger.exception("Error selecting SEND category for id {}".format(id))
            category = None

        return category

    def create_send_category(self, description, data):
        try:
            data_bin = encode_data(data)
            category = SENDCategory(description=description, data=data_bin)
            self.db.session.add(category)
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error creating SEND category '{}'".format(description))
            category = None

        return category

    def update_send_category(self, id, description, data):
        category = None

        try:
            data_bin = encode_data(data)
            self.db.session.query(SENDCategory).filter(SENDCategory.id == id).update(
                {
                    SENDCategory.description: description,
                    SENDCategory.data: data_bin
                })
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error updating SEND category '{}'".format(description))

        return category


    def get_send_user(self, tesla_id):
        try:
            categories = SENDCategory.query.filter(SENDCategory.id==LearnerSEND.category_id, LearnerSEND.tesla_id == str(tesla_id)).all()
        except:
            self.logger. exception("Error selecting SEND categories for a user")
            categories = None

        return categories

    def update_learner_send_categories(self, tesla_id, categories):
        try:
            self.db.session.query(LearnerSEND).filter(LearnerSEND.tesla_id == str(tesla_id)).delete()
            for cat in categories:
                new_cat = LearnerSEND(tesla_id=tesla_id, category_id=int(cat))
                self.db.session.add(new_cat)
            self.db.session.commit()
        except:
            self.logger. exception("Error updating SEND categories for a user. Rollback")
            self.db.session.rollback()

    def get_num_learners(self):
        try:
            num_learners = Learner.query.count()
        except:
            self.logger. exception("Error selecting number of learners")
            num_learners = 0

        return int(num_learners)

    def get_num_learners_no_ic(self):
        try:
            num_learners = Learner.query.filter(Learner.consent_id==None).count()
        except:
            self.logger. exception("Error selecting number of learners without informed consent")
            num_learners = 0

        return int(num_learners)

    def get_num_learners_valid_ic(self):
        try:
            version = self.get_current_informed_consent_version()
            if version is None:
                version = '0.0.0'
            version = '.'.join(version.split('.')[0:2])
            num_learners = Learner.query.filter(Learner.consent_rejected==None, Learner.consent_id==InformedConsent.id, InformedConsent.version.like(version + '.%')).count()
        except:
            self.logger. exception("Error selecting number of learners with valid informed consent")
            num_learners = 0

        return int(num_learners)

    def get_num_learners_rejected_ic(self):
        try:
            num_learners = Learner.query.filter(Learner.consent_rejected!=None).count()
        except:
            self.logger. exception("Error selecting number of learners with rejected informed consent")
            num_learners = 0

        return int(num_learners)

    def get_num_learners_outdated_ic(self):
        try:
            version = self.get_current_informed_consent_version()
            if version is None:
                version = '0.0.0'
            version = '.'.join(version.split('.')[0:2])
            num_learners = Learner.query.filter(Learner.consent_rejected==None, Learner.consent_id==InformedConsent.id, InformedConsent.version.notlike(version + '.%')).count()
        except:
            self.logger. exception("Error selecting number of learners with outdated informed consent")
            num_learners = 0
        return int(num_learners)

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

    def create_informed_consent(self, version, valid_from):
        try:
            ic = InformedConsent(version=version, valid_from=valid_from)
            self.db.session.add(ic)
            self.db.session.commit()
            self.db.session.refresh(ic)
        except Exception:
            self.logger.exception(
                "Error creating informed consent for version {} and valid_from {}".format(version, valid_from))
            self.db.session.rollback()
            return None

        return ic

    def get_informed_consent_by_version(self, version):
        try:
            ic = InformedConsent.query.filter(InformedConsent.version==version).one_or_none()
        except Exception:
            self.logger.exception("Error selecting informed consent by version for version={}".format(
                version))
            ic = None

        return ic

    def get_informed_consent_by_id(self, id):
        try:
            ic = InformedConsent.query.filter(InformedConsent.id==id).one_or_none()
        except Exception:
            self.logger.exception("Error selecting informed consent by id for id={}".format(
                id))
            ic = None

        return ic

    def get_current_informed_consent(self):
        try:
            ic = InformedConsent.query.filter(
                InformedConsent.valid_from <= datetime.datetime.now()
            ).order_by(InformedConsent.version.desc()).limit(1).one_or_none()
        except Exception:
            self.logger.exception("Error selecting current informed consent")
            ic = None

        return ic

    def get_current_informed_consent_version(self):
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

    def get_learner(self, tesla_id):
        try:
            learner = Learner.query.filter_by(tesla_id=tesla_id).one_or_none()
        except Exception:
            self.logger.exception("Error finding learner with id {}".format(tesla_id))
            learner = None

        return learner

    def get_learner_enrolment(self, tesla_id, instrument_id):
        try:
            enrolment = Enrollment.query.filter_by(tesla_id=tesla_id, instrument_id=instrument_id).one_or_none()
        except Exception:
            self.logger.exception("Error selecting learner enrolment for tesla_id and instrument_id {},{}".format(
                tesla_id, instrument_id))
            enrolment = None

        return enrolment

    def get_learner_pending_enrolment_requests(self, tesla_id, instrument_id):
        try:
            enrolment = Request.query.filter(Request.tesla_id == str(tesla_id),
                                             Request.instrument_list.like('%{}%'.format(instrument_id)),
                                             Request.is_enrolment == True,
                                             Request.status < 2).with_entities(Request.id,
                                                                               Request.start,
                                                                               Request.end,
                                                                               Request.status).all()
        except Exception:
            self.logger.exception(
                "Error selecting learner enrolment pending requests for tesla_id and instrument_id {},{}".format(
                    tesla_id, instrument_id))
            enrolment = None

        return enrolment

    def delete_learner_results(self, tesla_id):
        try:
            RequestResult.query.filter(RequestResult.request_id == Request.id, Request.tesla_id == str(tesla_id)).delete()
        except:
            self.logger. exception("Error removing request results for given learner")
            return False

        return True

    def delete_learner_audit_data(self, tesla_id):
        try:
            RequestAudit.query.filter(RequestAudit.request_id == Request.id, Request.tesla_id == str(tesla_id)).delete()
        except:
            self.logger. exception("Error removing request audit for given learner")
            return False

        return True

    def delete_learner_enrolment(self, tesla_id):
        try:
            Enrollment.query.filter(Enrollment.tesla_id == str(tesla_id)).delete()
        except:
            self.logger. exception("Error removing enrolment data for given learner")
            return False

        return True

    def delete_learner_enrolment_models(self, tesla_id):
        try:
            EnrollmentModel.query.filter(EnrollmentModel.tesla_id == str(tesla_id)).delete()
        except:
            self.logger. exception("Error removing enrolment models for given learner")
            return False

        return True

    def delete_learner_request_data(self, tesla_id):
        try:
            RequestData.query.filter(RequestData.request_id == Request.id, Request.tesla_id == str(tesla_id)).delete()
        except:
            self.logger. exception("Error removing request data for given learner")
            return False

        return True

    def delete_learner_requests(self, tesla_id):
        try:
            Request.query.filter(Request.tesla_id == str(tesla_id)).delete()
        except:
            self.logger. exception("Error removing requests for given learner")
            return False

        return True

    def delete_learner_send(self, tesla_id):
        try:
            LearnerSEND.query.filter(LearnerSEND.tesla_id == str(tesla_id)).delete()
        except:
            self.logger. exception("Error removing SEND data for given learner")
            return False

        return True

    def delete_learner(self, tesla_id):
        try:
            Learner.query.filter(Learner.tesla_id == str(tesla_id)).delete()
        except:
            self.logger. exception("Error removing given learner")
            return False

        return True

    def count_learner_pending_requests(self, tesla_id, enrolment, instrument_id):
        num_requests = Request.query.filter(Request.tesla_id == str(tesla_id), Request.is_enrolment == enrolment,
                                            Request.status == TESLA_REQUEST_STATUS.PENDING,
                                            Request.instrument_list.like('%{}%'.format(instrument_id))).count()

        return int(num_requests)

    def count_learner_completed_requests(self, tesla_id, enrolment, instrument_id):
        num_requests = Request.query.filter(Request.tesla_id == str(tesla_id), Request.is_enrolment == enrolment,
                                            Request.status == TESLA_REQUEST_STATUS.DONE,
                                            Request.instrument_list.like('%{}%'.format(instrument_id))).count()

        return int(num_requests)

    def count_learner_requests_by_status(self, tesla_id, enrolment, status, instrument_id):
        num_requests = Request.query.filter(Request.tesla_id == str(tesla_id), Request.is_enrolment == enrolment,
                                            Request.status == status,
                                            Request.instrument_list.like('%{}%'.format(instrument_id))).count()

        return int(num_requests)

    def get_learner_instrument_valid_results(self, tesla_id, instrument_id):
        results = RequestResult.query.filter(RequestResult.instrument_id==instrument_id,
                                             Request.id==RequestResult.request_id,
                                             Request.tesla_id == str(tesla_id),
                                             Request.is_enrolment==False,
                                             RequestResult.status==TESLA_RESULT_STATUS.DONE).all()

        return results

    def accept_informed_consent(self, tesla_id, consent_id):
        try:
            learner = self.db.session.query(Learner).filter(
                Learner.tesla_id == str(tesla_id)).with_for_update().one_or_none()
            if learner is None:
                return None

            learner.consent_rejected = None
            if learner.consent_id == consent_id:
                self.db.session.commit()
                self.db.session.refresh(learner)
                return learner

            learner.consent_id = consent_id
            learner.consent_accepted = datetime.datetime.now()

        except:
            self.logger. exception("Error accepting Informed Consent")
            self.db.session.rollback()
            learner = None

        return learner

    def reject_informed_consent(self, tesla_id):
        try:
            learner = self.db.session.query(Learner).filter(
                Learner.tesla_id == str(tesla_id)).with_for_update().one_or_none()
            if learner is None:
                return None

            learner.consent_rejected = datetime.datetime.now()
            self.db.session.commit()
            self.db.session.refresh(learner)
        except:
            self.logger. exception("Error rejecting Informed Consent")
            self.db.session.rollback()
            learner = None

        return learner

    def get_learner_courses(self, tesla_id):
        try:
            courses = Course.query.filter(Course.id==CourseLearner.course_id, CourseLearner.tesla_id == str(tesla_id)).all()
        except Exception:
            self.logger.exception(
                "Error selecting learner courses for tesla_id {}".format(tesla_id))
            courses = None

        return courses

    def get_learner_activities(self, tesla_id):
        try:
            activities = Activity.query.filter(Request.activity_id==Activity.id, Request.tesla_id == str(tesla_id)).all()
        except Exception:
            self.logger.exception(
                "Error selecting learner activities for tesla_id {}".format(tesla_id))
            activities = None

        return activities

    def count_learner_courses(self, tesla_id):
        try:
            num_courses = Course.query.filter(Course.id == CourseLearner.course_id,
                                          CourseLearner.tesla_id == str(tesla_id)).group_by(Course.id).count()
            if num_courses is None:
                num_courses = 0
            else:
                num_courses = int(num_courses)
        except Exception:
            self.logger.exception(
                "Error counting learner courses for tesla_id {}".format(tesla_id))
            num_courses = None

        return num_courses

    def count_learner_activities(self, tesla_id):
        try:
            num_activities = Activity.query.filter(Request.activity_id == Activity.id, Request.tesla_id == str(tesla_id)).group_by(Activity.id).count()
            if num_activities is None:
                num_activities = 0
            else:
                num_activities = int(num_activities)
        except Exception:
            self.logger.exception(
                "Error counting learner activities for tesla_id {}".format(tesla_id))
            num_activities = None

        return num_activities

    def get_learner_enrolments(self, tesla_id):
        try:
            enrolments = Enrollment.query.filter(Enrollment.tesla_id == str(tesla_id)).all()
        except Exception:
            self.logger.exception(
                "Error selecting learner enrolments for tesla_id {}".format(tesla_id))
            enrolments = None

        return enrolments

    """
    def get_learner_instrumentss(self, tesla_id):
        try:
            instruments = Instrument.query.filter(Request.tesla_id == str(tesla_id), RequestResult.request_id==Request.id).count()
            if num_requests is None:
                num_requests = 0
            else:
                num_requests = int(num_requests)
        except Exception:
            self.logger.exception(
                "Error selecting learner num requests per instrument for tesla_id {} and instrument {}".format(tesla_id, instrument_id))
            num_requests = None

        return num_requests
    """

    def count_learner_request_per_instruments(self, tesla_id, instrument_id, enrolment):
        try:
            num_requests = RequestResult.query.filter(Request.tesla_id == str(tesla_id),
                                                      Request.is_enrolment==enrolment,
                                                      RequestResult.request_id==Request.id,
                                                      RequestResult.instrument_id==instrument_id).count()
            if num_requests is None:
                num_requests = 0
            else:
                num_requests = int(num_requests)
        except Exception:
            self.logger.exception(
                "Error selecting learner num requests per instrument for tesla_id {} and instrument {}".format(tesla_id, instrument_id))
            num_requests = None

        return num_requests

