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

from flask_wtf import FlaskForm
from flask_babel import gettext
from wtforms import StringField, BooleanField, SubmitField, SelectMultipleField, HiddenField, IntegerField, widgets, PasswordField, validators
from wtforms.validators import DataRequired
from tesla_admin import tesla_db
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from tesla_models.models import Role

def get_roles():
    return lambda: Role.query.all()

def get_id(element):
    if type(element) is Role:
        return str(element.id)

    return str(element)

class UserForm(FlaskForm):
    roles_data = [(str(i.id), i.name) for i in tesla_db.users.get_roles()]

    username = StringField(gettext('Username'), validators=[DataRequired()], render_kw={"placeholder": gettext('Username')})
    email = StringField(gettext('Email'), validators=[DataRequired()], render_kw={"placeholder": gettext('Email')})
    active = BooleanField(gettext('Active'))
    roles = SelectMultipleField(gettext('Roles'), choices=roles_data, coerce=get_id)
    password = PasswordField(gettext('Password'), validators=[validators.EqualTo('repeat_password')])
    repeat_password = PasswordField(gettext('Repeat password'))

