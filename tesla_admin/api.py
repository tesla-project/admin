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

from flask import Blueprint, jsonify
from tesla_admin import tesla_data_provider, tesla_db
from tesla_admin.errors import not_found
from flask_security import roles_required, login_required, current_user

import time

api_learner = Blueprint('api_learner', __name__)


@api_learner.route('/find/<string:mail>', methods=['GET'])
@login_required
def find_learner(mail):

    learner = tesla_data_provider.find_learner(mail)
    if learner is None or (learner is not None and learner[0] is False):
        return not_found('Learner not found')

    info = tesla_data_provider.get_learner_data(learner[1], tep_sync=False)

    if info is None:
        return not_found('Cannot retrieve learner data')

    # Add mail information
    info['mail'] = mail

    return jsonify(info), 200


@api_learner.route('/alerts', methods=['GET'])
@login_required
def user_alerts():

    alerts = []
    return jsonify(alerts), 200


@api_learner.route('/messages', methods=['GET'])
@login_required
def user_messages():
    messages = tesla_db.users.get_user_pending_messages(current_user.id)
    return jsonify(messages), 200


@api_learner.route('/message/<int:message_id>', methods=['GET'])
@login_required
def get_user_message(message_id):
    message = tesla_db.users.get_message(message_id)
    if message is not None and message.user_id != current_user.id:
        return "Not authorized", 401
    return jsonify({"created": message.created, "id": message.id, "type": message.type, "subject": message.subject,
                    "content": message.content, "error_level": message.error_level}), 200


@api_learner.route('/message/<int:message_id>/read', methods=['GET'])
@login_required
def read_user_message(message_id):
    message = tesla_db.users.get_message(message_id)
    if message is not None and message.user_id != current_user.id:
        return "Not authorized", 401
    tesla_db.users.read_message(message_id)
    return jsonify([]), 200
