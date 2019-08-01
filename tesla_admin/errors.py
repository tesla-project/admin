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

from flask import request, jsonify


class TESLA_API_STATUS_CODE():
    SUCCESS = 0
    USER_NOT_FOUND = 1
    ERROR_DELETING_DATA = 2
    ACTIVITY_NOT_FOUND = 3
    REQUEST_NOT_FOUND = 4
    COMMUNICATION_ERROR = 5
    WORKER_EXCEPTION = 6
    INVALID_LEARNER_MODEL = 7
    SERVICE_EXCEPTION = 8
    NOT_ENOUGH_ENROLLMENT = 50
    ENROLLMENT_COMPLETE = 51
    INVALID_SAMPLE = 52
    INVALID_JSON = 53
    BAD_REQUEST = "BAD_REQUEST"

def abort(error=None):
    message = {
        'status': 404,
        'message': 'Abort: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


def access_denied():
    message = {
        'status': 401,
        'message': 'Access denied',
    }
    resp = jsonify(message)
    resp.status_code = 401

    return resp


def internal_error(error=None):
    message = {
        'status': 500,
        'message': 'Internal Error',
    }
    if error is not None:
        message['message'] += ': ' + str(error)
    resp = jsonify(message)
    resp.status_code = 500

    return resp
