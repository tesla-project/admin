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

from tesla_admin import celery, tesla_db
from tesla_models.constants import TESLA_RESULT_STATUS, TESLA_REQUEST_STATUS
import datetime


@celery.task(bind=True)
def import_course_data(self, task_id, course_id):
    # Executed on worker
    pass


@celery.task(bind=True)
def delete_learner_data(self, task_id, tesla_id):
    # Executed on worker
    pass

@celery.task(bind=True)
def delete_activity_data(self, task_id, activity_id):
    # Executed on worker
    pass

@celery.task()
def success_handler(task_result):
    # Executed on worker
    pass
