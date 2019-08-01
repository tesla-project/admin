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
from wtforms import StringField, DateTimeField, FileField, HiddenField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class InformedConsentForm(FlaskForm):
    version = StringField(gettext('Version'), validators=[DataRequired()], render_kw={"placeholder": gettext('Version')})
    valid_from = DateTimeField(gettext('Valid from'), validators=[DataRequired()], render_kw={"placeholder": gettext('Valid from')})
