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
from flask_wtf.form import _Auto
from flask_babel import gettext
from wtforms import StringField, BooleanField, SubmitField, SelectField, HiddenField, IntegerField, widgets, validators, ValidationError
from wtforms.fields.html5 import DateField

from tesla_admin import tesla_db

def unique_code_check(form, field):
    code = form.code.data
    id = form.id.data
    if code is None or len(code) == 0:
        raise ValidationError('Code must be provided')

    course = tesla_db.courses.get_course_by_code(code)
    if course is not None and course.id != int(id):
        raise ValidationError('Course code must be unique. This code is already used by another course.')


def get_vles():
    _vles = []
    vle_list = tesla_db.config.get_configured_vles()
    if vle_list is not None:
        _vles = [(str(vle.id), vle.name) for vle in vle_list]
    return _vles


def get_top_courses():
    _courses = [('-1' , '')]
    course_list = tesla_db.courses.get_active_top_courses()
    if course_list is not None:
        _courses = _courses + [(str(c.id), '[{}] - {}'.format(c.code, c.description)) for c in course_list]
    return _courses


def get_all_courses():
    _courses = [('-1' , '')]
    course_list = tesla_db.courses.get_active_courses()
    if course_list is not None:
        _courses = _courses + [(str(c.id), '[{}] - {}'.format(c.code, c.description)) for c in course_list]
    return _courses


class CourseForm(FlaskForm):

    def __init__(self, formdata=_Auto, **kwargs):
        super().__init__(formdata, **kwargs)
        self.update_dynamic_choices()


    id = IntegerField(widget=widgets.HiddenInput())
    #parent = SelectField(gettext('Parent Course'), choices=get_top_courses(), validators=(validators.Optional(),))
    parent = SelectField(gettext('Parent Course'), choices=get_all_courses(), validators=(validators.Optional(),))
    code = StringField(gettext('Code'), validators=[validators.DataRequired(), unique_code_check], render_kw={"placeholder": gettext('Course code')})
    description = StringField(gettext('Description'), validators=[validators.DataRequired()],
                              render_kw={"placeholder": gettext('Course description')})
    start = DateField('Start', format='%Y-%m-%d', validators=(validators.Optional(),))
    end = DateField('End', format='%Y-%m-%d', validators=(validators.Optional(),))
    vle_id = SelectField(gettext('VLE to connect'), choices=get_vles(), validators=(validators.Optional(),))
    vle_course_id = StringField(gettext('Course to connect'))
    submit = SubmitField(gettext('Save'))
    synchronize_vle = SubmitField(gettext('Synchronize with VLE'), default=None)
    delete = SubmitField(gettext('Delete'), default=None)

    def update_dynamic_choices(self):
        #self.parent.choices=get_top_courses()
        self.parent.choices = get_all_courses()
        self.vle_id.choices=get_vles()
