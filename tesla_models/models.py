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

from tesla_models import db, ma
from datetime import datetime
from flask_security import UserMixin, RoleMixin
from flask_security.utils import verify_password
from tesla_models.constants import TIES_RESULT_STATUS


class TimestampMixin(object):
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class TimestampStartEndMixin(object):
    start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end = db.Column(db.DateTime, onupdate=datetime.utcnow)


# Define the UserRoles association table
class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


# Define the Role data-model
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class RoleSchema(ma.ModelSchema):
    class Meta:
        model = Role

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)


# Define users model
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    locale = db.Column(db.String(10), default='en_GB')
    timezone = db.Column(db.String(15), default='UTC')
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary='roles_users',
                         backref=db.backref('users', lazy='dynamic'))

    def check_password(self, password):
        return verify_password(password, self.password)

    # Custom User Payload
    def get_security_payload(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'locale': self.locale,
            'timezone': self.timezone
        }


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'last_login_at', 'locale', 'timezone', 'active', 'confirmed_at', 'roles')

    roles = ma.Nested(RoleSchema, many=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Instrument(TimestampMixin, db.Model):
    __tablename__ = 'instrument'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False)
    acronym = db.Column(db.String, nullable=False, unique=True)
    url = db.Column(db.String, nullable=True)
    port = db.Column(db.Integer, nullable=True)
    active = db.Column(db.Boolean, nullable=False)
    has_licence = db.Column(db.Boolean, nullable=False, default=False)
    requires_enrollment = db.Column(db.Boolean, nullable=False, default=False)

    #activities = db.relationship("ActivityInstrument", back_populates="instruments")

    def __repr__(self):
        return "<Instrument(id='%d', name='%s', acronym='%s', url='%s', port='%r', active='%s')>" % (
            self.id, self.name, self.acronym, self.url, self.port, self.active)


db.Index('idx_instrument_acronym', Instrument.acronym.asc(), unique=True)


class Activity(TimestampMixin, db.Model):
    __tablename__ = 'activity'
    id = db.Column(db.BigInteger, primary_key=True)
    vle_id = db.Column(db.Integer, nullable=False)
    activity_type = db.Column(db.String, nullable=False)
    activity_id = db.Column(db.String, nullable=False)
    conf = db.Column(db.LargeBinary, nullable=True)
    description = db.Column(db.String, nullable=True)
    #instruments = db.relationship("ActivityInstrument", back_populates="activities")

    def __repr__(self):
        return "<Activity(id='%r', vle_id='%s', activity_type='%s', activity_id='%s')>" % (
            self.id, self.vle_id, self.activity_type, self.activity_id)


db.Index('idx_activity_type_activity_id', Activity.activity_id.asc(), Activity.activity_type.asc())


class InformedConsent(TimestampMixin, db.Model):
    __tablename__ = 'informed_consent'
    id = db.Column(db.BigInteger, primary_key=True)
    valid_from = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<InformedConsent(id='%d', version='%s', valid_from='%r')>" % (
            self.id, self.version, self.valid_from)


class InformedConsentSchema(ma.ModelSchema):
    class Meta:
        model = InformedConsent


informed_consent_schema = InformedConsentSchema()
informed_consents_schema = InformedConsentSchema(many=True)


class InformedConsentDocument(TimestampMixin, db.Model):
    __tablename__ = 'informed_consent_document'
    consent_id = db.Column(db.BigInteger, db.ForeignKey(InformedConsent.id), primary_key=True)
    language = db.Column(db.String(10), primary_key=True)
    html = db.Column(db.String, nullable=True)
    pdf = db.Column(db.LargeBinary, nullable=True)

    def __repr__(self):
        return "<InformedConsentDocument(consent_id='%d', language='%s')>" % (
            self.consent_id, self.language)


class InformedConsentDocumentSchema(ma.ModelSchema):
    class Meta:
        model = InformedConsentDocument


informed_consent_document_schema = InformedConsentDocumentSchema()
informed_consent_documents_schema = InformedConsentDocumentSchema(many=True)

class Learner(TimestampMixin, db.Model):
    __tablename__ = 'learner'
    tesla_id = db.Column(db.String(64), nullable=False, primary_key=True)
    crypto_data = db.Column(db.LargeBinary, nullable=True)
    consent_id = db.Column(db.BigInteger, db.ForeignKey(InformedConsent.id), nullable=True)
    consent_accepted = db.Column(db.DateTime, nullable=True)
    consent_rejected = db.Column(db.DateTime, nullable=True)
    def __repr__(self):
        return "<Learner(tesla_id='%r', consent_id='%r')>" % (
            self.tesla_id, self.consent_id)


class ActivityInstrument(db.Model):
    __tablename__ = 'activity_instrument'
    instrument_id = db.Column(db.BigInteger, db.ForeignKey(Instrument.id), primary_key=True)
    activity_id = db.Column(db.BigInteger, db.ForeignKey(Activity.id), primary_key=True)
    alternative_instrument_id = db.Column(db.BigInteger, db.ForeignKey(Instrument.id), nullable=True)
    required = db.Column(db.Boolean, nullable=False, default=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    options = db.Column(db.LargeBinary, nullable=True)
    alternative_options = db.Column(db.LargeBinary, nullable=True)

    #instrument = db.relationship("Instrument", back_populates="activities", foreign_keys=[instrument_id])
    #activity = db.relationship("Activity", back_populates="instruments", foreign_keys=[activity_id])

    def __repr__(self):
        return "<ActivityInstrument(activity_id='%r', instrument_id='%r', alternative='%r', required='%r', active='%r')>" % (
            self.activity_id, self.instrument_id, self.alternative_instrument_id, self.required, self.active)


class Request(TimestampMixin, db.Model, TimestampStartEndMixin):
    __tablename__ = 'request'
    id = db.Column(db.BigInteger, primary_key=True)
    tesla_id = db.Column(db.String(64), db.ForeignKey(Learner.tesla_id), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    activity_id = db.Column(db.BigInteger, db.ForeignKey(Activity.id), nullable=True)
    is_enrolment = db.Column(db.Boolean, nullable=True)
    instrument_list = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<Request(id='%r', tesla_id='%s', activity_id='%r', status='%r', is_enrollment='%r')>" % (
            self.id, self.tesla_id, self.activity_id, self.status, self.is_enrolment)

db.Index('idx_request_tesla_id', Request.tesla_id.asc())


class RequestData(TimestampMixin, db.Model):
    __tablename__ = 'request_data'
    request_id = db.Column(db.BigInteger, db.ForeignKey(Request.id), primary_key=True)
    data = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
        return "<RequestData(request_id='%r')>" % (self.request_id)


class RequestResult(TimestampMixin, db.Model, TimestampStartEndMixin):
    __tablename__ = 'request_result'
    instrument_id = db.Column(db.BigInteger, db.ForeignKey(Instrument.id), primary_key=True)
    request_id = db.Column(db.BigInteger, db.ForeignKey(Request.id), primary_key=True)
    result = db.Column(db.Numeric, nullable=True)
    detail = db.Column(db.String, nullable=True)
    error_code = db.Column(db.Numeric, nullable=True)
    error_message = db.Column(db.String, nullable=True)
    status = db.Column(db.Integer, nullable=False, default=0) # 0 => Pending, 1 => Started, 2 => Processed, 3 => Failed
    progress = db.Column(db.Numeric, nullable=False, default=0.0)
    num_retry = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return "<RequestResult(instrument_id='%d', request_id='%d', result='%r, error_code='%r', error_message='%r', status='%r', progress='%r')>" % (
            self.instrument_id, self.request_id, self.result, self.error_code, self.error_message, self.status, self.progress)

db.Index('idx_request_result_request_id', RequestResult.request_id.asc())


class RequestAudit(TimestampMixin, db.Model):
    __tablename__ = 'request_audit'
    instrument_id = db.Column(db.BigInteger, db.ForeignKey(Instrument.id), primary_key=True)
    request_id = db.Column(db.BigInteger, db.ForeignKey(Request.id), primary_key=True)
    enrolment = db.Column(db.Boolean, nullable=False, default=True)
    request = db.Column(db.Boolean, nullable=False, default=True)
    data = db.Column(db.LargeBinary, nullable=True)

    def __repr__(self):
        return "<RequestAudit(instrument_id='%d', request_id='%d', enrolment='%r', request='%r')>" % (
            self.instrument_id, self.request_id, self.enrolment, self.request)


class Enrollment(TimestampMixin, db.Model):
    __tablename__ = 'enrollment'
    tesla_id = db.Column(db.String(64), db.ForeignKey(Learner.tesla_id), primary_key=True)
    instrument_id = db.Column(db.BigInteger, db.ForeignKey(Instrument.id), primary_key=True)
    percentage = db.Column(db.Numeric, nullable=False, default=0.0)
    status = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return "<Enrollment(tesla_id='%s', instrument_id='%d', status='%r', percentage='%r')>" % (
            self.tesla_id, self.instrument_id, self.status, self.percentage)


db.Index('idx_enrollment_tesla_id', Enrollment.tesla_id.asc())


class EnrollmentModel(TimestampMixin, db.Model):
    __tablename__ = 'enrollment_model'
    tesla_id = db.Column(db.String(64), db.ForeignKey(Learner.tesla_id), primary_key=True)
    instrument_id = db.Column(db.BigInteger, db.ForeignKey(Instrument.id), primary_key=True)
    status = db.Column(db.Integer, nullable=False, default=0)
    locked = db.Column(db.Boolean, nullable=False, default=False)
    lock_date = db.Column(db.DateTime, nullable=True)
    lock_code = db.Column(db.String(64), nullable=True)
    data = db.Column(db.LargeBinary, nullable=True)

    def __repr__(self):
        return "<EnrollmentModel(tesla_id='%s', instrument_id='%d', status='%d', locked='%r')>" % (
            self.tesla_id, self.instrument_id, self.status, self.locked)


db.Index('idx_enrollment_model_tesla_id', EnrollmentModel.tesla_id.asc())


class InstrumentQueue(TimestampMixin, db.Model):
    __tablename__ = 'instrument_queue'
    instrument_id = db.Column(db.BigInteger, db.ForeignKey(Instrument.id), primary_key=True)
    queue = db.Column(db.String, nullable=False)
    consumers = db.Column(db.Integer, nullable=False, default=0)
    pending_tasks = db.Column(db.Integer, nullable=False, default=0)
    tendency1 = db.Column(db.Integer, nullable=False, default=0)
    tendency2 = db.Column(db.Integer, nullable=False, default=0)
    service = db.Column(db.Boolean, nullable=True, default=False)
    service_info = db.Column(db.String, nullable=True)

    def __repr__(self):
        return "<InstrumentQueue(instrument_id='%r', queue='%s', pending_tasks='%r', consumers='%r')>" % (
            self.instrument_id, self.queue, self.pending_tasks, self.consumers)


class InstrumentThresholds(TimestampMixin, db.Model):
    __tablename__ = 'instrument_thresholds'
    instrument_id = db.Column(db.BigInteger, db.ForeignKey(Instrument.id), primary_key=True)
    low = db.Column(db.Float, nullable=False)
    medium = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    audit_level = db.Column(db.String(6), nullable=False)

    def __repr__(self):
        return "<InstrumentThresholds(instrument_id='%r', low='%r', medium='%r', high='%r', audit_level='%r')>" % (
            self.instrument_id, self.low, self.medium, self.high, self.audit_level)


class TEPMigrations(TimestampMixin, db.Model):
    __tablename__ = 'tep_migrations'
    element = db.Column(db.String, primary_key=True)
    offset = db.Column(db.BigInteger, nullable=False, default=0)

    def __repr__(self):
        return "<TEPMigrations(element='%r', offset='%s')>" % (
            self.element, self.offset)


class SENDCategory(TimestampMixin, db.Model):
    __tablename__ = 'send_category'
    id = db.Column(db.BigInteger, primary_key=True)
    description = db.Column(db.String, nullable=False)
    data = db.Column(db.LargeBinary, nullable=True)

    def __repr__(self):
        return "<SENDCategory(id='%r', description='%s')>" % (
            self.id, self.description)


class LearnerSEND(TimestampMixin, db.Model):
    __tablename__ = 'learner_send'
    tesla_id = db.Column(db.String(64), db.ForeignKey(Learner.tesla_id), primary_key=True)
    category_id = db.Column(db.BigInteger, db.ForeignKey(SENDCategory.id), primary_key=True)
    expires = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return "<LearnerSEND(tesla_id='%r', category_id='%d')>" % (
            self.tesla_id, self.category_id)


class VLE(TimestampMixin, db.Model):
    __tablename__ = 'vle'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False)
    vle_id = db.Column(db.BigInteger, unique=True)
    url = db.Column(db.String, nullable=True)
    token = db.Column(db.String, nullable=True)

    def __repr__(self):
        return "<VLE(id='%r', vle_id='%r', name='%s')>" % (
            self.id, self.vle_id, self.name)


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    start = db.Column(db.DateTime, nullable=True)
    end = db.Column(db.DateTime, nullable=True)
    vle_id = db.Column(db.BigInteger, db.ForeignKey(VLE.id), nullable=True)
    vle_course_id = db.Column(db.String, nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)
    children = db.relationship("Course",
                            backref=db.backref('parent', remote_side=[id])
                            )

    learners = db.relationship('Learner', secondary='course_learner',
                            backref=db.backref('courses', lazy='dynamic'))

    activities = db.relationship('Activity', secondary='course_activity',
                               backref=db.backref('courses', lazy='dynamic'))

    def __repr__(self):
        return "<Course(id='%r', code='%s')>" % (
            self.id, self.code)


class CourseActivity(db.Model):
    __tablename__ = 'course_activity'
    course_id = db.Column(db.BigInteger, db.ForeignKey(Course.id), primary_key=True)
    activity_id = db.Column(db.BigInteger, db.ForeignKey(Activity.id), primary_key=True)

    def __repr__(self):
        return "<Course(id='%r', code='%s')>" % (
            self.id, self.code)


class CourseLearner(db.Model):
    __tablename__ = 'course_learner'
    course_id = db.Column(db.BigInteger, db.ForeignKey(Course.id), primary_key=True)
    tesla_id = db.Column(db.String(64), db.ForeignKey(Learner.tesla_id), primary_key=True)

    def __repr__(self):
        return "<Course(id='%r', code='%s')>" % (
            self.id, self.code)


class Configuration(TimestampMixin, db.Model):
    __tablename__ = 'configuration'
    key = db.Column(db.String(128), primary_key=True)
    description = db.Column(db.String, nullable=True)
    value = db.Column(db.String, nullable=True)

    def __repr__(self):
        return "<Configuration(key='%r', value='%r')>" % (
            self.key, self.value)


class Task(TimestampMixin, db.Model):
    __tablename__ = 'task'
    id = db.Column(db.BigInteger, primary_key=True)
    type = db.Column(db.String, nullable=False)
    task_id = db.Column(db.String(155), unique=False)
    status = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey(User.id), nullable=True)
    result = db.Column(db.LargeBinary, nullable=True)
    target_type = db.Column(db.String, nullable=True)
    target_id = db.Column(db.BigInteger, nullable=True)

    def __repr__(self):
        return "<Task(id='%r', task_id='%r', user_id='%r', status='%r')>" % (
            self.id, self.task_id, self.user_id, self.status)


class Message(TimestampMixin, db.Model):
    __tablename__ = 'message'
    id = db.Column(db.BigInteger, primary_key=True)
    type = db.Column(db.String, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey(User.id), nullable=False)
    subject = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    readAt = db.Column(db.DateTime, nullable=True)
    error_level = db.Column(db.Integer, nullable=True, default=0)

    def __repr__(self):
        return "<Message(id='%r', user_id='%r', type='%r', error_level='%r', readAt='%r')>" % (
            self.id, self.user_id, self.type, self.readAt)


class CourseSchema(ma.ModelSchema):
    class Meta:
        model = Course
        fields = ('id', 'vle_id', 'activity_type', 'activity_id', 'description')


course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)


class ActivitySchema(ma.ModelSchema):
    class Meta:
        model = Activity
        fields = ('id', 'vle_id', 'activity_type', 'activity_id', 'description')


activity_schema = ActivitySchema()
activities_schema = ActivitySchema(many=True)

class TiesService(TimestampMixin, db.Model):
    __tablename__ = 'ties_service'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return "<TiesService(id='%r', name='%s', code='%s', active='%s')>" % (
            self.id, self.name, self.code, self.active)


class TiesResult(TimestampMixin, db.Model):
    __tablename__ = 'ties_result'
    request_id = db.Column(db.BigInteger, db.ForeignKey(Request.id), nullable=True, primary_key=True)
    service_id = db.Column(db.BigInteger, db.ForeignKey(TiesService.id), nullable=True, primary_key=True)
    score = db.Column(db.LargeBinary, nullable=True)
    status = db.Column(db.Integer, nullable=False, default=TIES_RESULT_STATUS.RESULT_PENDING)
    error_message = db.Column(db.String, nullable=True)
    audit = db.Column(db.LargeBinary, nullable=True)

    request = db.relationship('Request')
    service = db.relationship('TiesService')

    def __repr__(self):
        return "<TiesResult(request_id='%r', service_id='%r', status='%r', error_message'%s')>" % (
            self.request_id, self.service_id, self.status, self.error_message)


class TiesConfig(TimestampMixin, db.Model):
    __tablename__ = 'ties_service_config'
    id = db.Column(db.BigInteger, primary_key=True)
    service_id = db.Column(db.BigInteger, db.ForeignKey(TiesService.id), nullable=True, primary_key=False)
    key = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)

    service = db.relationship('TiesService')

    def __repr__(self):
        return "<TiesServiceConfig(id='%r', service_id='%s', key='%s', value='%s')>" % (
            self.id, self.service_id, self.key, self.value)