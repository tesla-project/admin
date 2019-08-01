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
from wtforms import StringField, BooleanField, SubmitField, SelectField, HiddenField, IntegerField, widgets, validators
from wtforms.fields.html5 import URLField

from tesla_admin import tesla_db


class VLETokenForm(FlaskForm):
    id = IntegerField(widget=widgets.HiddenInput())
    name = StringField(gettext('Name'), validators=[validators.DataRequired()],
                              render_kw={"placeholder": gettext('VLE Name')})
    vle_id = StringField(gettext('VLE Id'), validators=[validators.DataRequired()],
                       render_kw={"placeholder": gettext('VLE Id')})
    token = StringField(gettext('Token'), render_kw={"placeholder": gettext('VLE Access Token')})
    url = URLField(gettext('URL'), render_kw={"placeholder": gettext('VLE url')})
    submit = SubmitField(gettext('Save'))
    delete = SubmitField(gettext('Delete'), default=None)
