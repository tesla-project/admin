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
from wtforms import StringField, BooleanField, SubmitField, SelectMultipleField, HiddenField, IntegerField, widgets
from wtforms.validators import DataRequired
from tesla_admin import tesla_db

class DivListWidget(widgets.ListWidget):

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = [] #['<%s %s>' % (self.html_tag, widgets.html_params(**kwargs))]
        for subfield in field:
            if self.prefix_label:
                html.append('<div class="i-checks">%s %s</div>' % (subfield.label, subfield(**kwargs)))
            else:
                html.append('<div class="i-checks">%s %s</div>' % (subfield(**kwargs), subfield.label))
        return widgets.HTMLString(''.join(html))


class MultiCheckboxField(SelectMultipleField):
    widget = DivListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class CategoryForm(FlaskForm):
    _options = [("hc", "High Contrast"), ("t2s", "Text to Speech"), ("bf", "Big Fonts")]
    _instruments = [(str(i.id), i.name) for i in tesla_db.instruments.get_instruments()]

    id = IntegerField(widget=widgets.HiddenInput())
    description = StringField(gettext('Description'), validators=[DataRequired()], render_kw={"placeholder": gettext('Category description')})
    options = MultiCheckboxField('Label', choices=_options)
    instruments = MultiCheckboxField('Label', choices=_instruments)
    submit = SubmitField(gettext('Save'))