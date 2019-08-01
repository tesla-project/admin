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

from tesla_models.models import Activity, ActivityInstrument, Request, RequestResult, RequestData, RequestAudit, Enrollment
from tesla_models.constants import TESLA_RESULT_STATUS
from sqlalchemy import asc, desc, or_, func, and_, funcfilter
from .utils import encode_data, decode_data


class ActivityDB(object):

    def __init__(self, db, logger):
        self.logger = logger
        self.db = db

    def create_activity(self, vle_id, activity_type, activity_id, config=None, description=None):
        try:
            bin_conf = encode_data(config)
            new_activity = Activity(vle_id=vle_id, activity_type=activity_type, activity_id=activity_id,
                                    conf=bin_conf, description=description)

            self.db.session.add(new_activity)
            self.db.session.commit()
            self.db.session.refresh(new_activity)
        except Exception:
            self.logger.exception("Error creating new activity {}".format(new_activity))
            new_activity = None

        return new_activity

    def update_activity_config(self, activity_id, config):
        try:
            bin_conf = encode_data(config)
            Activity.query.filter_by(id=activity_id)\
                .update({'conf': bin_conf})
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error updating activity config for activity {}".format(activity_id))
            return False

        return True

    def update_activity_description(self, activity_id, description):
        try:
            Activity.query.filter_by(id=activity_id)\
                .update({'description': description})
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error updating activity description for activity {}".format(activity_id))
            return False

        return True

    def update_activity_instruments(self, activity_id, instruments):
        try:
            current_instruments = self.db.session.query(ActivityInstrument).filter(
                ActivityInstrument.activity_id == activity_id
            ).with_for_update().all()

            # Disable current instruments
            for inst in current_instruments:
                inst.active = False

            # Update list of instruments
            for new_inst in instruments:
                found = False
                for inst in current_instruments:
                    if inst.instrument_id == new_inst['instrument_id']:
                        inst.active = True
                        inst.required = new_inst['required']
                        inst.alternative_instrument_id = new_inst['alternative_code']
                        found = True
                        break
                if not found:
                    added_inst = ActivityInstrument(activity_id=activity_id, instrument_id=new_inst['instrument_id'],
                                                    required=new_inst['required'], active=True,
                                                    alternative_instrument_id=new_inst['alternative_code'])
                    self.db.session.add(added_inst)
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error updating activity instruments for activity {}. Rollback.".format(activity_id))
            self.db.session.rollback()
            return False

        return True

    def get_activity(self, activity_id):
        try:
            activity = Activity.query.filter_by(id=activity_id).one_or_none()
        except Exception:
            self.logger.exception("Error selecting activity for id {}".format(activity_id))
            activity = None

        return activity

    def get_activity_by_def(self, vle_id, activity_type, activity_id):
        try:
            activity = Activity.query.filter_by(vle_id=vle_id, activity_type=activity_type,
                                                activity_id=activity_id).one_or_none()
        except Exception:
            self.logger.exception("Error selecting activity for vle_id, activity_type, activity_id {},{},{}".format(
                vle_id, activity_type, activity_id))
            activity = None

        return activity

    def get_activity_instruments(self, activity_id):
        try:
            current_instruments = ActivityInstrument.query.filter(
                ActivityInstrument.activity_id == activity_id,
                ActivityInstrument.active == True
            ).all()

        except Exception:
            self.logger.exception("Error getting activity instruments for activity {}. Rollback.".format(activity_id))
            return None

        return current_instruments

    def get_activity_results(self, tesla_id, activity_id):
        try:
            results = RequestResult.query.filter(
                RequestResult.request_id==Request.id,
                Request.tesla_id==tesla_id,
                Request.activity_id==activity_id
            ).order_by(Request.id).all()

        except Exception:
            self.logger.exception("Error getting activity results for a learner.")
            return []

        return results

    def delete_activity_results(self, activity_id):
        try:
            RequestResult.query.filter(RequestResult.request_id == Request.id, Request.activity_id == activity_id).delete()
        except:
            self.logger.exeption("Error removing request results for activity {}".format(activity_id))
            return False

        return True

    def delete_activity_audit_data(self, activity_id):
        try:
            RequestAudit.query.filter(RequestAudit.request_id == Request.id, Request.activity_id == activity_id).delete()
        except:
            self.logger.exeption("Error removing request audit for activity {}".format(activity_id))
            return False

        return True

    def delete_activity_request_data(self, activity_id):
        try:
            RequestData.query.filter(RequestData.request_id == Request.id, Request.activity_id == activity_id).delete()
        except:
            self.logger.exeption("Error removing request data for activity {}".format(activity_id))
            return False

        return True

    def delete_activity_requests(self, activity_id):
        try:
            Request.query.filter(Request.activity_id == activity_id).delete()
        except:
            self.logger.exeption("Error removing requests for activity {}".format(activity_id))
            return False

        return True

    def delete_activity_instruments(self, activity_id):
        try:
            ActivityInstrument.query.filter(ActivityInstrument.activity_id == activity_id).delete()
        except:
            self.logger.exeption("Error removing instrument assignment for activity {}".format(activity_id))
            return False

        return True

    def delete_activity(self, activity_id):
        try:
            Activity.query.filter(Activity.id == activity_id).delete()
        except:
            self.logger.exeption("Error removing activity {}".format(activity_id))
            return False

        return True

    def get_activities(self, q=None, limit=None, offset=0, sort='id', order='asc'):
        results = []
        try:
            if sort is '' or sort is None:
                sort = 'id'

            if q is not None and q is not '':
                q = '%'+str(q)+'%'
                query = Activity.query.filter(or_(Activity.description.like(q), Activity.activity_type.like(q)))
            else:
                query = Activity.query

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

    def count_activities(self, q=None, limit=None, offset=0):
        result = 0
        try:
            if q is not None:
                q = '%'+str(q)+'%'
                query = Activity.query.filter(or_(Activity.description.like(q), Activity.activity_type.like(q)))
            else:
                query = Activity.query

            query = query.offset(offset)

            if limit is not None:
                query = query.limit(limit)

            result = query.count()

        except Exception:
            self.logger.exception("Error getting activities count")

        return result

    def get_activity_results(self, activity_id, pagination=None):
        results = []
        try:
            query = self.db.session.query(Request, RequestResult).filter(RequestResult.request_id==Request.id, Request.activity_id==activity_id)

            if pagination is not None:
                results = pagination.get_results(query)
            else:
                results = query.all()

        except Exception:
            self.logger.exception("Error getting list of activities")

        return results

    def get_activity_learners_with_results(self, activity_id, pagination=None):
        results = []
        try:
            query = self.db.session.query(Request.tesla_id).filter(RequestResult.request_id==Request.id, Request.activity_id==activity_id).group_by(Request.tesla_id)

            if pagination is not None:
                results = pagination.get_results(query)
            else:
                results = query.all()

        except Exception:
            self.logger.exception("Error getting list of activities")

        return results

    def get_activity_instruments_with_results(self, activity_id):
        try:
            results = self.db.session.query(RequestResult.instrument_id).filter(RequestResult.request_id==Request.id, Request.activity_id==activity_id).group_by(RequestResult.instrument_id).all()
        except Exception:
            self.logger.exception("Error getting list of instruments used in a activity")
            results = None

        return results

    def get_activity_learner_summary(self, activity_id, tesla_id):

        try:
            summary = self.db.session.query(
                RequestResult.instrument_id,
                func.max(Enrollment.percentage).label('enrolment_percentage'),
                funcfilter(func.count(1), RequestResult.status==TESLA_RESULT_STATUS.DONE).label('valid'),
                funcfilter(func.count(1), RequestResult.status == TESLA_RESULT_STATUS.PENDING).label('pending'),
                funcfilter(func.count(1), or_(RequestResult.status == TESLA_RESULT_STATUS.TIMEOUT, RequestResult.status== TESLA_RESULT_STATUS.FAILED)).label('failed'),
                funcfilter(func.min(RequestResult.result), RequestResult.status==TESLA_RESULT_STATUS.DONE).label('min'),
                funcfilter(func.max(RequestResult.result), RequestResult.status == TESLA_RESULT_STATUS.DONE).label('max'),
                funcfilter(func.avg(RequestResult.result), RequestResult.status == TESLA_RESULT_STATUS.DONE).label('average')
            ).filter(
                Request.tesla_id==tesla_id,
                Request.activity_id == activity_id,
                RequestResult.request_id == Request.id
            ).outerjoin(Enrollment,
                        and_(Enrollment.tesla_id==tesla_id,
                            Enrollment.instrument_id==RequestResult.instrument_id)
            ).group_by(
                RequestResult.instrument_id
            ).all()
        except Exception:
            self.logger.exception("Error getting summary for a learner and activity")
            summary = None

        return summary

    def get_activity_summary(self, activity_id):

        try:
            summary = self.db.session.query(
                RequestResult.instrument_id,
                func.avg(Enrollment.percentage).label('enrolment_percentage'),
                funcfilter(func.count(1), RequestResult.status==TESLA_RESULT_STATUS.DONE).label('valid'),
                funcfilter(func.count(1), RequestResult.status == TESLA_RESULT_STATUS.PENDING).label('pending'),
                funcfilter(func.count(1), or_(RequestResult.status == TESLA_RESULT_STATUS.TIMEOUT, RequestResult.status== TESLA_RESULT_STATUS.FAILED)).label('failed'),
                funcfilter(func.min(RequestResult.result), RequestResult.status==TESLA_RESULT_STATUS.DONE).label('min'),
                funcfilter(func.max(RequestResult.result), RequestResult.status == TESLA_RESULT_STATUS.DONE).label('max'),
                funcfilter(func.avg(RequestResult.result), RequestResult.status == TESLA_RESULT_STATUS.DONE).label('average')
            ).filter(
                Request.activity_id == activity_id,
                RequestResult.request_id == Request.id
            ).outerjoin(Enrollment,
                            Enrollment.instrument_id==RequestResult.instrument_id
            ).group_by(
                RequestResult.instrument_id
            ).all()
        except Exception:
            self.logger.exception("Error getting summary for an activity")
            summary = None

        return summary
