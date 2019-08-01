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

from flask import Blueprint, jsonify, url_for, render_template, request
from tesla_admin.decorators import certificate_required
from tesla_admin import logger, tesla_db, tesla_data_provider
from tesla_admin.helpers import api_response
from tesla_admin.errors import TESLA_API_STATUS_CODE
from tesla_models.database.utils import decode_data, ResultsPagination
from datetime import datetime
import time
from flask_security import roles_required, login_required

stats = Blueprint('stats', __name__, template_folder='templates', static_folder='static')

@stats.route('/learners', methods=['GET'])
@login_required
@roles_required('Statistics')
def learners_stats():

    return render_template('learners_stats.html', page = 'stats.learners')


@stats.route('/activities', methods=["GET"])
@login_required
@roles_required('Statistics')
def activities():

    return render_template('activities.html', page = 'stats.activities')

@stats.route('/courses', methods=["GET"])
@login_required
@roles_required('Statistics')
def courses():


    return render_template('courses.html', page = 'stats.courses')


@stats.route('/rt', methods=["GET"])
@login_required
@roles_required('Statistics')
def rt():

    return render_template('rt.html', page = 'stats.rt')


@stats.route('/courses/active/learners', methods=["GET"])
@login_required
@roles_required('Statistics')
def list_active_top_course_learners_ajax():

    learner_stats = tesla_db.statistics.get_active_top_course_learner_statistics(paginate=ResultsPagination(request))

    learner_stats['rows'] = learner_stats.pop('items')

    return jsonify(learner_stats), 200


@stats.route('/rt/stats', methods=["GET"])
@login_required
@roles_required('Statistics')
def rt_stats():
    stats = {
        'learners': {
            'total': tesla_db.learners.get_num_learners(),
            'ic_ok': tesla_db.learners.get_num_learners_valid_ic(),
            'no_ic': tesla_db.learners.get_num_learners_no_ic(),
            'ic_rejected': tesla_db.learners.get_num_learners_rejected_ic(),
            'ic_outdated': tesla_db.learners.get_num_learners_outdated_ic()
        },
        'requests': {
            'enrolment': {
                'pending': tesla_db.requests.get_num_requests_pending(True),
                'processed': tesla_db.requests.get_num_requests_processed(True),
                'failed': tesla_db.requests.get_num_requests_failed(True)
            },
            'verification': {
                'pending': tesla_db.requests.get_num_requests_pending(False),
                'processed': tesla_db.requests.get_num_requests_processed(False),
                'failed': tesla_db.requests.get_num_requests_failed(False)
            }
        }
    }

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, {'timestamp': datetime.now(), 'stats': stats})


@stats.route('/course/<int:course_id>/stats', methods=["GET"])
@login_required
@roles_required('Statistics')
def course_stats(course_id):

    stats = {
        'num_learners': tesla_db.statistics.num_learners_course(course_id),
        'num_activities': tesla_db.statistics.num_activities_course(course_id)
    }

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, {'stats': stats})


@stats.route('/course/<int:course_id>/stats/instruments', methods=["GET"])
@login_required
@roles_required('Statistics')
def list_course_instruments_ajax(course_id):
    num_learners = tesla_db.statistics.num_learners_course(course_id)
    stats = []
    instruments = tesla_db.statistics.instruments_course(course_id)
    for inst_id in instruments:
        inst = tesla_db.instruments.get_instrument_by_id(inst_id)

        inst_stats = {
            'acronym': inst.acronym.upper(),
            'name': inst.name,
            'requires_enrolment': inst.requires_enrollment,
            'learners_verification_requests': tesla_db.statistics.num_course_learners_with_verification_requests(course_id, inst_id),
            'learners_verification_stats': tesla_db.statistics.verification_course_results_histogram(course_id, inst_id)
        }
        if inst.requires_enrollment:
            inst_stats['learners_enrolment_completed'] = tesla_db.statistics.num_course_learners_enrolment_complete(course_id, inst_id)
            inst_stats['learners_enrolment_started'] = tesla_db.statistics.num_course_learners_enrolment_started(course_id, inst_id)
            inst_stats['learners_enrolment_empty'] = num_learners - (inst_stats['learners_enrolment_completed'] + inst_stats['learners_enrolment_started'])

        stats.append(inst_stats)

    return jsonify(stats), 200


def _get_course_learners_badge(course_id):
    badges = ''

    course_stats = tesla_db.statistics.get_course_learner_statistics(course_id)

    total_learners = course_stats.total
    valid_ic_learners = course_stats.valid_ic
    outdated_ic_learners = course_stats.outdated_ic
    rejected_ic_learners = course_stats.rejected_ic
    no_ic_learners = course_stats.no_ic

    badge_format = '<span class="badge badge-{}"><span class="badge badge-pill badge-light">{}</span><span class="sr-only">{}</span></span>'
    if total_learners > 0:
        badges += badge_format.format('dark', total_learners, 'total learners')
    if valid_ic_learners > 0:
        badges += badge_format.format('success', valid_ic_learners, 'learners with valid informed consent')
    if outdated_ic_learners > 0:
        badges += badge_format.format('warning', outdated_ic_learners, 'learners with outdated informed consent')
    if rejected_ic_learners > 0:
        badges += badge_format.format('danger', rejected_ic_learners,  'learners with rejected informed consent')
    if no_ic_learners > 0:
        badges += badge_format.format('info', no_ic_learners,  'learners with no informed consent')

    return badges


@stats.route('/course/tree', methods=["GET"])
@login_required
@roles_required('Statistics')
def get_course_tree():

    parent_id = request.args.get('parentId')
    if parent_id is not None:
        parent = tesla_db.courses.get_course(int(parent_id))
        courses = parent.children
    else:
        courses = tesla_db.courses.get_active_top_courses()

    nodes = []

    for c in courses:
        has_children = len(c.children) > 0
        has_activities = len(c.activities) > 0
        if has_activities:
            icon = "fas fa-graduation-cap"
        else:
            icon = "fas fa-folder"

        nodes.append({
            "id": c.id,
            "text": "<b>[{}]</b> - {} {}".format(c.code, c.description, _get_course_learners_badge(c.id)),
            "parent_id": c.parent_id,
            "hasChildren": has_children,
            "imageCssClass": icon
        })

    return jsonify(nodes), 200


def _get_course_activity_badge(course_id):
    badges = ''

    course_stats = tesla_db.statistics.get_course_learner_statistics(course_id)
    num_activities = tesla_db.statistics.num_activities_course(course_id)

    total_learners = course_stats.total

    badge_format = '<span class="badge badge-{}"><span class="badge badge-pill badge-light">{}</span><span class="sr-only">{}</span></span>'
    if total_learners > 0:
        badges += badge_format.format('dark', total_learners, 'number of learners')
    if num_activities > 0:
        badges += badge_format.format('success', num_activities, 'number of activities')

    return badges


@stats.route('/activity/<int:activity_id>/stats', methods=["GET"])
@login_required
@roles_required('Statistics')
def activity_stats(activity_id):

    stats = {
        #'num_learners': 0tesla_db.statistics.num_learners_course(course_id),
        #'num_instruments': tesla_db.statistics.num_activities_course(course_id)
    }

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, {'stats': stats})


@stats.route('/activity/tree', methods=["GET"])
@login_required
@roles_required('Statistics')
def get_activity_tree():

    parent_id = request.args.get('parentId')
    parent = None
    if parent_id is not None:
        parent = tesla_db.courses.get_course(int(parent_id))
        courses = parent.children
    else:
        courses = tesla_db.courses.get_active_top_courses()

    nodes = []

    for c in courses:
        has_children = len(c.children) > 0 or len(c.activities) > 0
        num_activities = tesla_db.statistics.num_activities_course(c.id)
        if num_activities > 0:
            if len(c.activities) > 0:
                icon = "fas fa-graduation-cap"
            else:
                icon = "fas fa-folder"

            nodes.append({
                "id": c.id,
                "text": "<b>[{}]</b> - {} {}".format(c.code, c.description, _get_course_activity_badge(c.id)),
                "parent_id": c.parent_id,
                "hasChildren": has_children,
                "imageCssClass": icon,
                "type": "course"
            })
    if parent is not None:
        for a in parent.activities:

            nodes.append({
                "id": a.id,
                "text": "<b>[{} - {} - {}]</b> - {}".format(a.vle_id, a.activity_type, a.activity_id, a.description),
                "parent_id": parent.id,
                "hasChildren": False,
                "imageCssClass": "fas fa-tasks",
                "type": "activity"
            })


    return jsonify(nodes), 200


@stats.route('/activity/<int:activity_id>/stats/instruments', methods=["GET"])
@login_required
@roles_required('Statistics')
def list_activity_instruments_ajax(activity_id):

    activity = tesla_db.activities.get_activity(activity_id)
    if activity is None:
        jsonify([]), 404
    courses = list(activity.courses)
    if len(courses)==1:
        num_learners = tesla_db.statistics.num_learners_course(courses[0].id)

    stats = []
    instruments = tesla_db.statistics.instruments_activity(activity_id)
    for inst_id in instruments:
        inst = tesla_db.instruments.get_instrument_by_id(inst_id)

        inst_stats = {
            'acronym': inst.acronym.upper(),
            'name': inst.name,
            'requires_enrolment': inst.requires_enrollment,
            'learners_verification_requests': tesla_db.statistics.num_activity_learners_with_verification_requests(activity_id, inst_id),
            'learners_verification_stats': tesla_db.statistics.verification_activity_results_histogram(activity_id, inst_id)
        }
        if inst.requires_enrollment:
            inst_stats['learners_enrolment_completed'] = tesla_db.statistics.num_activity_learners_enrolment_complete(activity_id, inst_id)
            inst_stats['learners_enrolment_started'] = tesla_db.statistics.num_activity_learners_enrolment_started(activity_id, inst_id)
            inst_stats['learners_enrolment_empty'] = num_learners - (inst_stats['learners_enrolment_completed'] + inst_stats['learners_enrolment_started'])

        stats.append(inst_stats)

    return jsonify(stats), 200