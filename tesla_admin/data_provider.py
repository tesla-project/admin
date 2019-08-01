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

from tesla_admin import tesla_db, current_user, logger, tip_api_connect
from flask_babelex import gettext, format_date
from tesla_models import tep_db
import uuid
from datetime import datetime
import requests
from distutils.version import LooseVersion

def get_learner_ic_info(tesla_id, tep_sync=True):

    response = {'learner_found': False,
                'ic_version': None,
                'ic_current_version': None,
                'accepted_date': None,
                'rejected_date': None,
                'ic_valid': False
                }

    # Get the learner information
    if tep_sync:
        # TODO: Remove if TEP is not deployed
        learner = tep_db.sync_learner(tesla_id)
    else:
        learner = tesla_db.learners.get_learner(tesla_id)

    if learner is None:
        return response

    response['learner_found']= True

    # Get informed consent information
    if learner.consent_id is None:
        return response

    ic = tesla_db.learners.get_informed_consent_by_id(learner.consent_id)
    current_ic = tesla_db.learners.get_current_informed_consent()
    response['ic_version'] = ic.version
    response['accepted_date'] = learner.consent_accepted
    response['rejected_date'] = learner.consent_rejected
    response['ic_current_version'] = current_ic.version

    if learner.consent_rejected is not None:
        return response

    ic_version = LooseVersion(ic.version).version
    current_version = LooseVersion(current_ic.version).version

    if ic_version[0] == current_version[0] and ic_version[1] == current_version[1]:
        response['ic_valid'] = True

    return response


class TeSLADataProvider(object):

    _current_user = None
    _db = None

    @property
    def current_user(self):
        if self._current_user is None:
            self._current_user = current_user
        return self._current_user

    @property
    def db(self):
        if self._db is None:
            self._db = tesla_db
        return self._db

    def get_user_context(self):
        return {
            'notifications': self.get_notifications(),
            'messages':self. get_messages()
        }

    def get_notifications(self):
        notification = {
            'type': 'alert',
            'created_at': datetime.utcnow(),
            'message': 'dddd'
        }

        return [notification]

    def get_messages(self):
        return tesla_db.users.get_user_pending_messages(current_user.id)

    def find_learner(self, mail):
        if not tip_api_connect.exists(mail):
            return None

        return tip_api_connect.get_tesla_id(mail)

    def get_learner_data(self, tesla_id, tep_sync=True):
        #send = tesla_db.learners.get_send_user(tesla_id)
        ic_info = get_learner_ic_info(tesla_id, tep_sync=tep_sync)

        if ic_info['ic_valid']:
            if ic_info['ic_version']==ic_info['ic_current_version']:
                ic_message = gettext("Valid. Version %(version)s accepted on %(date)s", version=ic_info['ic_version'],
                                     date=ic_info['accepted_date'])
            else:
                ic_message = gettext("Valid with old version. Version %(version)s accepted on %(date)s. Current version is %(new_version)", version=ic_info['ic_version'],
                                     date=ic_info['accepted_date'], new_version=ic_info['ic_current_version'])
            ic_status = 'correct'
        else:
            if ic_info['rejected_date'] is not None:
                ic_message = gettext("Rejected")
                ic_status = 'rejected'
            elif ic_info['accepted_date'] is not None:
                ic_message = gettext("Outdated. Version %(version)s was accepted on %(date)s. New version %(new_version)s must be accepted.", version=ic_info['ic_version'],
                                     date=ic_info['accepted_date'], new_version=ic_info['ic_current_version'])
                ic_status = 'outdated'
            else:
                ic_message = gettext(
                    "Pending. No informed consent accepted yet.")
                ic_status = 'pending'

        info = {
            'tesla_id': tesla_id,
            #'send': send,
            'ic_message': ic_message,
            'ic_status' : ic_status,
            'ic_valid': ic_info['ic_valid']
        }
        return info

