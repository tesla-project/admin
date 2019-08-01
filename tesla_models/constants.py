
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

class TESLA_API_REQUEST_MODE():
    ENROLLMENT = 0
    VERIFICATION = 1

class TESLA_REQUEST_STATUS():
    PENDING = 0
    RUNNING = 1
    DONE = 2
    FAILED = 3
    TIMEOUT = 4

class TESLA_RESULT_STATUS():
    PENDING = 0
    RUNNING = 1
    DONE = 2
    FAILED = 3
    TIMEOUT = 4

class TESLA_ENROLLMENT_PHASE():
    NOT_STARTED = 1
    ONGOING = 2
    COMPLETED = 3

class TESLA_MESSAGE_TYPE():
    TASK_CREATED = "TASK_CREATED"
    TASK_STARTED = "TASK_STARTED"
    TASK_SUCCEED = "TASK_SUCCEED"
    TASK_FAILED = "TASK_FAILED"

class TIES_RESULT_STATUS():
    RESULT_PENDING = 1
    RESULT_PROCESSING = 2
    RESULT_ERROR = 3
    RESULT_END = 0