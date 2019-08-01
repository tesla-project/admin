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

import re
from flask import jsonify

BLOB_RE = re.compile('(?:timestamp:[^;]+;)?(?:filename:[^;]+;)?data:([^;]+)?(?:;base64)?,(.*)')
BLOB_RE_OLD = re.compile('(?:timestamp:[^,]+,)?(?:filename:[^,]+,)?data:([^;]+)?(?:;base64)?,(.*)')

def api_response(status_code, data= None, http_code=200):
    """
        Create the response for API methods

        :param status_code: Status code value from the ones defined in TESLA_API_STATUS_CODE
        :type status_code: int
        :param data: Dictionary with all the data to be sent in the response
        :type data: dictionary
        :param http_code: HTTP status code
        :type http_code: int
        :return: tuple expected as response to API calls (content, http_status)
    """
    json_data = { 'status_code': '{}'.format(status_code)}
    if data is not None:
        json_data.update(data)
    return jsonify(json_data), http_code


def parse_request_data(request_data):
    matches = BLOB_RE.match(request_data)
    if not matches:
        matches = BLOB_RE_OLD.match(request_data)
        if not matches:
            return None
        else:
            file_name = None
            timestamp = None
            if request_data.startswith('timestamp'):
                timestamp = request_data.split(',')[0]
                if request_data.split(',')[1].startswith('filename'):
                    file_name = request_data.split(',')[1].split(',')[0]
            elif request_data.startswith('filename'):
                file_name = request_data.split(',')[0]
    else:
        file_name = None
        timestamp = None
        if request_data.startswith('timestamp'):
            timestamp = request_data.split(';')[0]
            if request_data.split(';')[1].startswith('filename'):
                file_name = request_data.split(';')[1].split(';')[0]
        elif request_data.startswith('filename'):
            file_name = request_data.split(';')[0]

    if file_name is not None:
        file_name = file_name.split(':')[1]

    mime_type = matches.group(1)
    b64_data = str(matches.group(2))

    return {
        'file_name': file_name,
        'mime_type': mime_type,
        'b64_data': b64_data,
        'timestamp': timestamp
    }


def load_class(name):
    #try:
    #    components = name.split('.')

    #    mod = __import__('.'.join(components[0:-1]), fromlist=[components[-1]])
    #    return getattr(mod, components[-1])
    #except AttributeError:
    #    return None
    import importlib
    try:
        class_inst = None
        components = name.split('.')
        expected_class = components[-1]
        expected_module = '.'.join(components[0:-1])
        module = importlib.import_module(expected_module)
        class_inst = getattr(module, expected_class)
    except:
        return None

    return class_inst
