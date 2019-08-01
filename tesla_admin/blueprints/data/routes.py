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

from flask import Blueprint, jsonify, url_for, render_template, request, redirect
from flask_security import roles_required, login_required, current_user, roles_accepted
from tesla_admin.decorators import certificate_required
from tesla_admin import logger, tesla_db
from tesla_admin.helpers import api_response
from tesla_admin.errors import TESLA_API_STATUS_CODE
from .forms import CourseForm
from tesla_models import models
from tesla_models.constants import TESLA_MESSAGE_TYPE, TESLA_REQUEST_STATUS
from tesla_admin import tasks
from flask_babelex import gettext

data = Blueprint('data', __name__, template_folder='templates', static_folder='static')


@data.route('/learner', methods=['GET'])
@login_required
@roles_required('Admin')
def learner():
    return render_template('learner.html', page= 'data.learner')


@data.route('/activity', methods=['GET'])
@login_required
@roles_required('Admin')
def activity():
    return render_template('activity.html', page= 'data.activity')


@data.route('/course', methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def course():
    form = CourseForm()
    has_errors = True
    if form.validate_on_submit():
        parent_id = form.data.get('parent')
        if parent_id == 'None':
            parent_id = None
        if parent_id is not None:
            parent_id = int(parent_id)
            if parent_id < 0:
                parent_id = None
        if form.data.get('submit') or form.data.get('synchronize_vle'):
            if form.data["id"] < 0:
                new_course = tesla_db.courses.create_course(code=form.data.get('code'), description=form.data.get('description'),
                                            start=form.data.get('start'), end=form.data.get('end'),
                                            vle_id=form.data.get('vle_id'), vle_course_id=form.data.get('vle_course_id'),
                                            parent_id=parent_id)
                form.id.data = new_course.id
                form.id.raw_data = [str(new_course.id)]
            else:
                if parent_id == form.data.get('id'):
                    parent_id = None
                tesla_db.courses.update_course(id=form.data.get('id'), code=form.data.get('code'),
                                               description=form.data.get('description'),
                                               start=form.data.get('start'), end=form.data.get('end'),
                                               vle_id=form.data.get('vle_id'),
                                               vle_course_id=form.data.get('vle_course_id'),
                                               parent_id=parent_id)
            has_errors = False

        if form.data.get('delete'):
            if tesla_db.courses.delete_course(form.data["id"]):
                return redirect(url_for('data.course'))

        if form.data.get('synchronize_vle'):
            course_to_sync = tesla_db.courses.get_child_courses_with_synch_data(int(form.id.data))

            for c in course_to_sync:
                if c.vle_course_id == '':
                    continue
                # Create a new task
                new_task = tesla_db.tasks.create_task(type="IMPORT_VLE_DATA", user_id=current_user.id)
                tasks.import_course_data.apply_async([new_task.id, c.id], priority=5)
                # Create a message to the user
                tesla_db.users.create_message(user_id=current_user.id, type=TESLA_MESSAGE_TYPE.TASK_CREATED,
                                              subject=gettext('New task created'), content=gettext(
                        "A new task to import all data from the course %(value)s has been created. This can take several hours depending on the system load. You will be notified.",
                                              value=c.description))

    if request.method == "GET":
        has_errors = False

    courses = tesla_db.courses.get_active_courses()
    form.update_dynamic_choices()

    return render_template('course.html', page='data.course', form=form, courses=courses, has_errors=has_errors)


@data.route('/course/<int:id>', methods=['GET'])
@login_required
@roles_required('Admin')
def get_course_data(id):
    course = tesla_db.courses.get_course(id)
    if course is None:
        return api_response(TESLA_API_STATUS_CODE.REQUEST_NOT_FOUND, http_code=404)

    parent_id = -1
    if course.parent_id is not None:
        parent_id = course.parent_id

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, {'id': course.id, 'description': course.description,
                                                        'code': course.code, 'start': course.start, 'end': course.end,
                                                        'vle_id': course.vle_id, 'vle_course_id': course.vle_course_id,
                                                        'parent_id': parent_id})


@data.route('/course/<int:id>/activities', methods=['GET'])
@login_required
@roles_required('Admin')
def list_selected_activities_ajax(id):
    q = request.args.get('search')
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    sort = request.args.get('sort')
    order = request.args.get('order')

    list_activities_data = tesla_db.courses.get_activities(course_id=id, q=q, limit=limit,
                                                                     offset=offset, order=order, sort=sort)
    total_activities = tesla_db.courses.count_activities(course_id=id, q=q)

    activities_data = models.courses_schema.dump(list_activities_data)

    return_data = {
        'total': total_activities,
        'rows': activities_data[0]
    }

    return jsonify(return_data), 200


@data.route('/course/<int:id>/available_activities', methods=['GET'])
@login_required
@roles_required('Admin')
def list_available_activities_ajax(id):
    q = request.args.get('search')
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    sort = request.args.get('sort')
    order = request.args.get('order')

    list_activities_data = tesla_db.courses.get_available_activities(course_id=id, q=q, limit=limit, offset=offset,
                                                                     order=order, sort=sort)
    total_activities = tesla_db.courses.count_available_activities(course_id=id, q=q)

    activities_data = models.courses_schema.dump(list_activities_data)

    return_data = {
        'total': total_activities,
        'rows': activities_data[0]
    }

    return jsonify(return_data), 200


@data.route('/course/<int:course_id>/activity/<int:activity_id>', methods=['DELETE', 'POST'])
@login_required
@roles_required('Admin')
def course_activity(course_id, activity_id):

    if request.method == "DELETE":
        tesla_db.courses.delete_activity(course_id, activity_id)

    if request.method == "POST":
        tesla_db.courses.add_activity(course_id, activity_id)

    return api_response(TESLA_API_STATUS_CODE.SUCCESS)


@data.route('/learner/data/<string:tesla_id>', methods=["GET"])
@login_required
@roles_accepted('Admin', 'Statistics')
def get_learner_data_summary(tesla_id):

    summary = {
        'tesla_id': tesla_id,
        'courses': tesla_db.learners.count_learner_courses(tesla_id),
        'activities': tesla_db.learners.count_learner_activities(tesla_id)
    }

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, summary)


@data.route('/learner/<string:tesla_id>', methods=["DELETE"])
@login_required
@roles_required('Admin')
def delete_learner(tesla_id):
    # Create a new task
    new_task = tesla_db.tasks.create_task(type="DELETE_LEARNER_DATA", user_id=current_user.id)
    tasks.delete_learner_data.apply_async([new_task.id, tesla_id], priority=5)
    # Create a message to the user
    tesla_db.users.create_message(user_id=current_user.id, type=TESLA_MESSAGE_TYPE.TASK_CREATED,
                                  subject=gettext('New task created'), content=gettext(
            "A new task to delete all data from user %(value)s has been created. This can take several hours depending on the system load. You will be notified.",
            value=tesla_id))

    return api_response(TESLA_API_STATUS_CODE.SUCCESS)


@data.route('/activity/<string:activity_id>', methods=["DELETE"])
@login_required
@roles_required('Admin')
def delete_activity(activity_id):
    # Create a new task
    new_task = tesla_db.tasks.create_task(type="DELETE_ACTIVITY_DATA", user_id=current_user.id)
    tasks.delete_activity_data.apply_async([new_task.id, activity_id], priority=5)
    # Create a message to the user
    tesla_db.users.create_message(user_id=current_user.id, type=TESLA_MESSAGE_TYPE.TASK_CREATED,
                                  subject=gettext('New task created'), content=gettext(
            "A new task to delete all data for activity %(value)s has been created. This can take several hours depending on the system load. You will be notified.",
            value=activity_id))

    return api_response(TESLA_API_STATUS_CODE.SUCCESS)


@data.route('/activities', methods=['GET'])
@login_required
@roles_required('Admin')
def list_activities_ajax():
    q = request.args.get('search')
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    sort = request.args.get('sort')
    order = request.args.get('order')

    list_activities_data = tesla_db.activities.get_activities(q=q, limit=limit, offset=offset,
                                                                     order=order, sort=sort)
    total_activities = tesla_db.activities.count_activities(q=q)

    activities_data = models.activities_schema.dump(list_activities_data)

    return_data = {
        'total': total_activities,
        'rows': activities_data[0]
    }

    return jsonify(return_data), 200


@data.route('/learner/<string:tesla_id>/instruments', methods=['GET'])
@login_required
@roles_required('Admin')
def list_learner_instruments_ajax(tesla_id):
    instruments = tesla_db.instruments.get_instruments()
    instrument_data = []
    for inst in instruments:
        enrolment = None
        if inst.requires_enrollment:
            enrolment = 0.0
            enrol_row = tesla_db.learners.get_learner_enrolment(tesla_id, inst.id)
            if enrol_row is not None:
                enrolment = enrol_row.percentage

        inst_results_histogram = tesla_db.statistics.get_learner_instrument_valid_results_histogram(tesla_id, inst.id)
        instrument_data.append({
            'acronym': inst.acronym,
            'name': inst.name,
            'enrolment': enrolment,
            'results': inst_results_histogram,
            'requests': {
                'enrolment': {
                    'processed': tesla_db.learners.count_learner_completed_requests(tesla_id, True, inst.id),
                    'pending': tesla_db.learners.count_learner_pending_requests(tesla_id, True, inst.id),
                    'failed': tesla_db.learners.count_learner_requests_by_status(tesla_id, True,
                                                                                 TESLA_REQUEST_STATUS.FAILED, inst.id),
                    'timeout': tesla_db.learners.count_learner_requests_by_status(tesla_id, True,
                                                                                  TESLA_REQUEST_STATUS.FAILED, inst.id)
                },
                'verification': {
                    'processed': tesla_db.learners.count_learner_completed_requests(tesla_id, False, inst.id),
                    'pending': tesla_db.learners.count_learner_pending_requests(tesla_id, False, inst.id),
                    'failed': tesla_db.learners.count_learner_requests_by_status(tesla_id, False,
                                                                                 TESLA_REQUEST_STATUS.FAILED, inst.id),
                    'timeout': tesla_db.learners.count_learner_requests_by_status(tesla_id, False,
                                                                                  TESLA_REQUEST_STATUS.FAILED, inst.id)
                }
            }
        })

    return jsonify(instrument_data), 200
