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

from marshmallow import Schema, fields, ValidationError, post_load
from tesla_admin.helpers import parse_request_data


class SampleData(fields.Field):
    def _serialize(self, value, attr, obj):
        return super(SampleData, self)._serialize(value)

    def _validate(self, value):
        if value is None:
            raise ValidationError('Invalid format.')

    def deserialize(self, value, attr=None, data=None):
        sample_data = parse_request_data(value)
        self._validate(sample_data)
        return sample_data


class TeSLAID(fields.UUID):

    def deserialize(self, value, attr=None, data=None):
        value = super(TeSLAID, self).deserialize(value, attr, data)
        return str(value)


class ActivitySchema(Schema):
    vle_id = fields.Integer(required=True)
    activity_type = fields.String(required=True)
    activity_id = fields.String(required=True)


class NewValidationSchema(Schema):
    tesla_id = TeSLAID(required=True)
    evaluation_id = fields.Integer(required=True)
    activity = fields.Nested(ActivitySchema, required=False)
    sample_data = SampleData(required=True)


class NewEnrollmentSchema(Schema):
    tesla_id = TeSLAID(required=True)
    enrolment_id = fields.Integer(required=True)
    sample_data = SampleData(required=True)


class ActivityConfigSchema(ActivitySchema):
    config = fields.String(required=False)


def validate(schema, request):
    try:
        result = schema.load(request.get_json())
        valid = not bool(result.errors)
        valid_data = result.data
        errors = result.errors
    except ValidationError as err:
        valid = False
        errors = err.messages
        valid_data = err.valid_data

    return valid, valid_data, errors


def validate_new_evaluation(request):
    return validate(NewValidationSchema(), request)


def validate_new_enrollment(request):
    return validate(NewEnrollmentSchema(), request)


def validate_activity_config(request):
    return validate(ActivityConfigSchema, request)
