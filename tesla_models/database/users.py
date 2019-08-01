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

from tesla_models.models import User, RolesUsers, Role, Message
from sqlalchemy import asc, desc, or_
from flask_security.utils import hash_password
from flask_security import current_user
from datetime import datetime

class UserDB(object):

    def __init__(self, db, logger):
        self.logger = logger
        self.db = db

    def user_exists(self, user_name):
        try:
            result = User.query.filter(User.username == user_name).one_or_none()
        except:
            return False

        return result is not None

    def get_user_count(self):
        result = 0
        try:
            result = self.db.session.query(User).count()
        except Exception:
            self.logger.exception("Error selecting SEND categories")

        return result

    def get_users(self, q=None, limit=None, offset=0, sort='id', order='asc'):
        results = []
        try:
            if sort is '' or sort is None:
                sort = 'id'

            if q is not None and q is not '':
                q = '%'+str(q)+'%'
                query = User.query.filter(or_(User.email.like(q), User.username.like(q)))
            else:
                query = User.query

            if order == 'asc':
                query = query.order_by(asc(sort))
            else:
                query = query.order_by(desc(sort))

            query = query.offset(offset)

            if limit is not None:
                query = query.limit(limit)

            results = query.all()

        except Exception:
            self.logger.exception("Error getting list users")

        return results

    def get_user(self, id):
        result = None
        try:
            result = User.query.filter(User.id == id).first()
        except Exception:
            self.logger.exception("Error getting list users")

        return result

    def user_addedit(self, id, form):
        result = False
        try:
            if id is 0:
                password = hash_password(form.data.get('password'))
                user = User(username=form.data.get('username'), email=form.data.get('email'),
                            active=form.data.get('active'), password=password)
                self.db.session.add(user)
                self.db.session.commit()

                id = user.id
            else:
                self.db.session.query(User).filter(User.id == id).update(
                    {
                        User.email: form.data.get('email'),
                        User.username: form.data.get('username'),
                        User.active: form.data.get('active')
                    })
                self.db.session.commit()
                if form.data.get('password') is not None and form.data.get('password') is not '':
                    password = hash_password(form.data.get('password'))
                    self.db.session.query(User).filter(User.id == id).update(
                        {
                            User.password: password,
                        })
                    self.db.session.commit()

            # delete all user roles, and assign the new ones
            user_roles = RolesUsers.query.filter(RolesUsers.user_id == id).all()

            for ur in user_roles:
                self.db.session.delete(ur)
                self.db.session.commit()

            for role in form.data.get('roles'):
                user_roles = RolesUsers(user_id=id, role_id=role)
                self.db.session.add(user_roles)
                self.db.session.commit()

            result = True
        except Exception:
            self.logger.exception("Error getting addedit user")

        return result

    def user_delete(self, id=None):
        try:
            if current_user is not None and str(current_user.id) == str(id):
                return False

            if id is not None:
                user = User.query.filter(User.id == id).first()
                self.db.session.delete(user)
                self.db.session.commit()
                return True
        except Exception:
            self.logger.exception("Error deleting user")

        return False

    def count_users(self, q=None, limit=None, offset=0):
        result = 0
        try:
            if q is not None:
                q = '%'+str(q)+'%'
                query = User.query.filter(or_(User.email.like(q), User.username.like(q)))
            else:
                query = User.query

            query = query.offset(offset)

            if limit is not None:
                query = query.limit(limit)

            result = query.count()

        except Exception:
            self.logger.exception("Error getting list users")

        return result

    def get_roles(self):
        try:
            roles = Role.query.all()
        except Exception:
            self.logger.exception("Error finding roles")
            roles = []

        return roles

    def create_message(self, user_id, type, subject, content, error_level=None):
        try:
            new_message = Message(type=type, user_id=user_id, subject=subject, content=content, error_level=error_level)

            self.db.session.add(new_message)
            self.db.session.commit()
            self.db.session.refresh(new_message)
        except Exception:
            self.logger.exception("Error creating {} message for user{}".format(type, user_id))
            new_message = None

        return new_message

    def read_message(self, message_id):
        try:
            Message.query.filter_by(id=message_id) \
                .update({
                    'readAt': datetime.now()
                })
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error updating read status for message with id {}".format(message_id))
            return False
        return True

    def read_all_user_messages(self, user_id):
        try:
            Message.query.filter_by(user_id=user_id, readAt=None) \
                .update({
                    'readAt': datetime.now()
                })
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error updating read status for all message for user with id {}".format(user_id))
            return False
        return True

    def get_message(self, message_id):
        try:
            msg = Message.query.filter_by(id=message_id).one_or_none()
        except Exception:
            self.logger.exception("Error getting message with id {}".format(message_id))
            return None
        return msg

    def get_user_messages(self, user_id):
        try:
            msg = Message.query.filter_by(user_id=user_id).order_by(Message.created.desc()).all()
        except Exception:
            self.logger.exception("Error getting messages for user id {}".format(user_id))
            return None
        return msg

    def get_user_pending_messages(self, user_id):
        try:
            msg = Message.query.filter(Message.user_id==user_id,
                                       Message.readAt==None).order_by(Message.created.desc()).all()
        except Exception:
            self.logger.exception("Error getting pending messages for user id {}".format(user_id))
            return None
        return msg
