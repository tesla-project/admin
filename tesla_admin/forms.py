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

from wtforms import StringField, validators
from flask_security import RegisterForm
from tesla_admin import tesla_db

class ExtendedRegisterForm(RegisterForm):
    username = StringField('Username', [validators.DataRequired(message='Username not provided'), validators.Regexp('[a-z0-9_-]{4,20}$', message='Wrong Username format')])

    def validate(self):
        #check for username
        if tesla_db.users.user_exists(self.username.data.strip()):
            self.username.errors += ("Username already taken", )
            return False

        #now check for Flask-Security validate functions
        if not super(ExtendedRegisterForm, self).validate():
            return False

        return True
