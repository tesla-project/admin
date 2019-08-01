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

from marshmallow import Schema, fields, ValidationError, pre_load
from .helpers import parse_request_data


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


class ActivityPropertiesSchema(Schema):
    description = fields.String(required=False, default=None)
    config = fields.Raw(required=False)


class ActivitySchema(ActivityPropertiesSchema):
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


class InstrumentSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    acronym = fields.String(required=True, load_from='description')
    version = fields.String(required=True)
    requires_enrollment = fields.Boolean(required=True, load_from='requiresEnrollment')
    status = fields.Integer(required=True)
    has_licence = fields.Boolean(required=True, load_from='hasLicence')
    active = fields.Boolean(required=True, load_from='deployed')
    url = fields.String(required=False, allow_none=True)
    port = fields.Integer(required=False, allow_none=True)


class VLESchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    version = fields.String(required=True)
    status = fields.Integer(required=True)


class VLEActivitySchema(Schema):
    activityId = fields.String(required=True)
    activityType = fields.String(required=True)
    name = fields.String(required=True)

    @pre_load(pass_many=True)
    def id_conversion(self, data, many):
        if many:
            for d in data:
                d['activityId'] = str(d['activityId'])
        else:
            data['activityId'] = str(data['activityId'])
        return data


class VLELearnerSchema(Schema):
    id = fields.Integer(required=True)
    email = fields.String(required=True)


class TEPNewRequest(Schema):
    sample_data = SampleData(required=True)


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


def validate_response(schema, response):
    try:
        result = schema.load(response.json())
        valid = not bool(result.errors)
        valid_data = result.data
        errors = result.errors
    except ValidationError as err:
        valid = False
        errors = err.messages
        valid_data = err.valid_data

    return valid, valid_data, errors


def validate_json(schema, json):
    try:
        result = schema.load(json)
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
    return validate(NewValidationSchema(), request)


def validate_portal_instruments(json):
    return validate_json(InstrumentSchema(many=True), json)


def validate_portal_vles(json):
    return validate_json(VLESchema(many=True), json)


def validate_vle_activities(json):
    return validate_json(VLEActivitySchema(many=True), json)


def validate_vle_learners(json):
    return validate_json(VLELearnerSchema(many=True), json)


def validate_new_tep_request(request):
    return validate(TEPNewRequest(), request)


