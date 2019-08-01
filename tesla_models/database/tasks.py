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

from tesla_models.models import Task, User
from sqlalchemy import asc, desc, or_
from celery import states

class TaskDB(object):

    def __init__(self, db, logger):
        self.logger = logger
        self.db = db

    def create_task(self, type, task_id=None, status=states.PENDING, user_id=None, result=None):
        try:
            new_task = Task(type=type, task_id=task_id, status=status, user_id=user_id, result=result)

            self.db.session.add(new_task)
            self.db.session.commit()
            self.db.session.refresh(new_task)
        except Exception:
            self.logger.exception("Error creating new task {}".format(task_id))
            new_task = None

        return new_task

    def update_task(self, id, type, task_id, status, user_id=None, result=None):
        try:
            Task.query.filter_by(id=id) \
                .update({
                    'type': type,
                    'task_id': task_id,
                    'status': status,
                    'user_id': user_id,
                    'result': result
                })
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error updating task with id {}".format(id))
            return False
        return True

    def start_task(self, id, task_id, status=states.STARTED):
        try:
            Task.query.filter_by(id=id) \
                .update({
                    'status': status,
                    'task_id': task_id
                })
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error closing task with id {}".format(id))
            return False
        return True

    def close_task(self, id, status, result=None):
        try:
            Task.query.filter_by(id=id) \
                .update({
                    'status': status,
                    'result': result
                })
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error closing task with id {}".format(id))
            return False
        return True

    def get_task(self, id):
        try:
            task = Task.query.filter_by(id=id).one_or_none()
        except Exception:
            self.logger.exception("Error getting task with id {}".format(id))
            return None
        return task

