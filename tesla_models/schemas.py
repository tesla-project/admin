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
from tesla_models import db, ma
from tesla_models import models
from tesla_models.database.utils import encode_data, decode_data


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


class Dictionary(fields.Raw):
    def _serialize(self, value, attr, obj):
        return super(Dictionary, self)._serialize(decode_data(value), attr, obj)

    def deserialize(self, value, attr=None, data=None):
        enc_data = encode_data(value)
        self._validate(enc_data)
        return enc_data


class Activity(ma.ModelSchema):
    class Meta:
        model = models.Activity
    conf = Dictionary(required=False, default=None)


class Instrument(ma.ModelSchema):
    class Meta:
        model = models.Instrument


class ActivityInstrument(ma.ModelSchema):
    class Meta:
        model = models.ActivityInstrument

    options = Dictionary(required=False, default=None)
    alternative_options = Dictionary(required=False, default=None)
    instrument_id = fields.Integer(required=True)
    alternative_instrument_id = fields.Integer(required=False, default=None)
    # TODO: See how to deal with BigInteger fields


class Request(ma.ModelSchema):
    class Meta:
        model = models.Request

    id = fields.Integer(required=True)
    activity_id = fields.Integer(required=True)


class RequestResult(ma.ModelSchema):
    class Meta:
        model = models.RequestResult

    instrument_id = fields.Integer(required=True)
    request_id = fields.Integer(required=True)


class Pagination(ma.ModelSchema):
    has_next = fields.Boolean(required=True)
    has_prev = fields.Boolean(required=True)
    next_num = fields.Integer(required=False)
    page = fields.Integer(required=True)
    pages = fields.Integer(required=True)
    per_page = fields.Integer(required=True)
    prev_num = fields.Integer(required=False)
    total = fields.Integer(required=True)
    items = fields.Raw(required=True)


class InstrumentResultsSummary(ma.ModelSchema):
    instrument_id = fields.Integer(required=True)
    min = fields.Number(required=None)
    max = fields.Number(required=None)
    average = fields.Number(required=None)
    valid = fields.Integer(required=True, default=0)
    failed = fields.Integer(required=True, default=0)


class ActivitySummary(ma.ModelSchema):
    tesla_id = TeSLAID(required=True, attribute='tesla_id')


class ActivitySummaryPagination(Pagination):
    items = fields.Nested(ActivitySummary, many=True, required=True)


class CourseLearnersStats(ma.ModelSchema):
    id = fields.Integer(required=True)
    code = fields.String(required=True)
    description = fields.String(required=False)
    start = fields.Date(required=False, default=None)
    end = fields.Date(required=False, default=None)
    total = fields.Integer(required=False, default=0)
    valid_ic = fields.Integer(required=False, default=0)
    rejected_ic = fields.Integer(required=False, default=0)
    no_ic = fields.Integer(required=False, default=0)
    outdated_ic = fields.Integer(required=False, default=0)


class LearnerInstrumentResults(ma.ModelSchema):
    instrument_id = fields.Integer(required=True)
    enrolment_percentage = fields.Number(required=None, default=0)
    min = fields.Number(required=None)
    max = fields.Number(required=None)
    average = fields.Number(required=None)
    valid = fields.Integer(required=True, default=0)
    pending = fields.Integer(required=True, default=0)
    failed = fields.Integer(required=True, default=0)


class LearnerResults(ma.ModelSchema):
    tesla_id = TeSLAID(required=True, attribute='tesla_id')
    instruments = fields.Nested(LearnerInstrumentResults, many=True, required=True)


class LearnerResultsPaginated(Pagination):
    items = fields.Nested(LearnerResults, many=True, required=True)


class CourseLearnersStatsPagination(Pagination):
    items = fields.Nested(CourseLearnersStats, many=True, required=True)


class Request_RequestResult(ma.ModelSchema):
    tesla_id = TeSLAID(required=True, attribute='Request.tesla_id')
    result = fields.Nested(RequestResult, required=True, attribute='RequestResult')


class RequestResultPagination(Pagination):
    items = fields.Nested(Request_RequestResult, many=True, required=True)
