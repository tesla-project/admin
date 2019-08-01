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

from flask import Blueprint, jsonify, url_for, render_template, request, send_from_directory
from tesla_admin.decorators import certificate_required
from tesla_admin import logger, tesla_db, tesla_data_provider, app
from tesla_admin.helpers import api_response
from tesla_admin.errors import TESLA_API_STATUS_CODE
from tesla_models.database.utils import decode_data, ResultsPagination
import tesla_models.schemas as schemas
from tesla_models import tep_db
from datetime import datetime, timedelta
import time
import base64
from flask_security import roles_required, login_required
from flask_sqlalchemy import Pagination
#from xhtml2pdf import pisa
import io
import os
import math
import simplejson
from tesla_admin.instrument_api import InstrumentAPI


reports = Blueprint('reports', __name__, template_folder='templates', static_folder='static')

def create_pdf(pdf_data):
    pdf = io.BytesIO()

    with open(os.path.join(reports.static_folder, 'css', 'reports.css'), 'r') as f:
        report_css = f.read()
#    pisa.CreatePDF(io.StringIO(pdf_data), dest=pdf)
    return pdf


@reports.route('/', methods=['GET'])
@login_required
@roles_required('Statistics')
def reports_index():

    pdf = create_pdf(render_template('reports/sample.html'))
    pdf_b64 = base64.b64encode(pdf.getvalue()).decode()

    return render_template('report_list.html', page = 'reports.list', pdf_b64=pdf_b64)


def _get_learner_instrument_stats(learner_result, context_statistics):

    learner_stats = {}
    learner_stats['instruments'] = {}
    auth_levels = []
    content_levels = []
    security_levels = []
    for instrument_id in context_statistics.keys():
        # Initialize the instrument statistics
        level = 0.0
        prob_learner = 0.0
        prob_context = 0.0
        h_prob_learner = 1.0
        h_prob_context = 1.0
        confidence = 0.0
        histogram = []
        result_bean = None

        # TODO: Put polarity in instrument fields
        instrument_polarity = 1
        if instrument_id in [6]:
            instrument_polarity = -1

        # TODO: Put properties in instrument fields
        if instrument_id in [1, 3, 5]:
            is_auth = True
            is_content = False
            is_security = False
        elif instrument_id in [7]:
            is_auth = True
            is_content = True
            is_security = False
        elif instrument_id in [2, 3]:
            is_auth = False
            is_content = False
            is_security = True
        elif instrument_id in [6]:
            is_auth = False
            is_content = True
            is_security = False
        else:
            is_auth = False
            is_content = False
            is_security = False

        # If learner have data for this instrument, update the statistics
        if instrument_id in learner_result['instruments']:
            context_hist = context_statistics[instrument_id]['histogram']
            histogram = tesla_db.statistics.get_learner_instrument_valid_results_histogram(learner_result['tesla_id'],
                                                                                       instrument_id)

            confidence = learner_result['instruments'][instrument_id]['valid'] / (learner_result['instruments'][instrument_id]['valid'] + learner_result['instruments'][instrument_id]['failed'] + 0.00000001)

            if confidence < 0.5:
                level = 2
            else:
                # Compute a final level
                if learner_result['instruments'][instrument_id]['average'] < 1.0:
                    result_bean = math.floor(learner_result['instruments'][instrument_id]['average']*10.0)
                else:
                    result_bean = 9

                if result_bean == 0:
                    prob_learner = (histogram[result_bean] + 0.5 * histogram[result_bean + 1]) / (sum(histogram) + 0.00000001)
                    prob_context = (context_hist[result_bean] + 0.5 * context_hist[result_bean + 1]) / (sum(context_hist) + 0.00000001)
                    if instrument_polarity > 0:
                        h_prob_learner = sum(histogram[1:10]) / (sum(histogram) + 0.00000001)
                        h_prob_context = sum(context_hist[1:10]) / (sum(context_hist) + 0.00000001)
                    else:
                        h_prob_learner = 0.0
                        h_prob_context = 0.0
                elif result_bean == 9:
                    prob_learner = (histogram[result_bean] + 0.5 * histogram[result_bean - 1]) / (sum(histogram) + 0.00000001)
                    prob_context = (context_hist[result_bean] + 0.5 * context_hist[result_bean - 1]) / (sum(context_hist) + 0.00000001)
                    if instrument_polarity > 0:
                        h_prob_learner = 0.0
                        h_prob_context = 0.0
                    else:
                        h_prob_learner = sum(histogram[0:9]) / (sum(histogram) + 0.00000001)
                        h_prob_context = sum(context_hist[0:9]) / (sum(context_hist) + 0.00000001)

                else:
                    prob_learner = (0.5 * histogram[result_bean - 1] + histogram[result_bean] + 0.5 * histogram[result_bean + 1]) / (sum(histogram) + 0.00000001)
                    prob_context = (0.5 * context_hist[result_bean - 1] + context_hist[result_bean] + 0.5 * context_hist[result_bean + 1]) / (sum(context_hist) + 0.00000001)
                    if instrument_polarity > 0:
                        h_prob_learner = sum(histogram[result_bean + 1:10]) / (sum(histogram) + 0.00000001)
                        h_prob_context = sum(context_hist[result_bean+1:10]) / (sum(context_hist) + 0.00000001)
                    else:
                        h_prob_learner = sum(histogram[0:result_bean]) / (sum(histogram) + 0.00000001)
                        h_prob_context = sum(context_hist[0:result_bean]) / (sum(context_hist) + 0.00000001)

                # Get instrument thresholds
                thresholds = context_statistics[instrument_id]['thresholds']

                # Build final recomendation
                if thresholds is not None:
                    if (instrument_polarity > 0 and learner_result['instruments'][instrument_id]['average'] > thresholds.medium) or \
                            (instrument_polarity < 0 and (1.0 - learner_result['instruments'][instrument_id]['average']) > thresholds.medium):
                        # If the mean value is in the green side, assume that is the learner
                        level = 3
                    else:
                        # Compare with the context
                        if h_prob_learner > 0.75:
                            # If the obtained value is not usual at all for this learner, assume that is not the learner
                            level = 1
                        elif h_prob_context < 0.5:
                            # If the value is larger than the contextual value, put in warning
                            level = 2
                        else:
                            # Otherwise put in danger
                            level = 1
                else:
                    # Compare with the context
                    if h_prob_learner < 0.4 and h_prob_context < 0.4:
                        level = 3
                    elif h_prob_learner > 0.75:
                        # If the obtained value is not usual at all for this learner, assume that is not the learner
                        level = 1
                    elif h_prob_context < 0.5:
                        # If the value is larger than the contextual value, put in warning
                        level = 2
                    else:
                        # Otherwise put in danger
                        level = 1

        # Store the instrument statistics
        learner_stats['instruments'][instrument_id] = {
            'prob_learner': prob_learner,
            'prob_context': prob_context,
            'h_prob_learner': h_prob_learner,
            'h_prob_context': h_prob_context,
            'confidence': confidence,
            'level': level,
            'instrument_polarity': instrument_polarity,
            'histogram': histogram,
            'result_bean': result_bean,
            'thresholds': context_statistics[instrument_id]['thresholds']
        }

        # Store the level
        if is_auth:
            auth_levels.append(level)
        if is_content:
            content_levels.append(level)
        if is_security:
            security_levels.append(level)

    # Compute a final levels
    if len(auth_levels) > 0:
        positive = 3 in auth_levels
        negative = 1 in auth_levels

        if positive and negative:
            auth_level = 2
        elif not positive and negative:
            auth_level = 1
        elif positive and not negative:
            auth_level = 3
        else:
            auth_level = math.floor(sum(auth_levels) / len(auth_levels))
    else:
        auth_level = 0

    if len(content_levels) > 0:
        positive = 3 in content_levels
        negative = 1 in content_levels

        if positive and negative:
            content_level = 2
        elif not positive and negative:
            content_level = 1
        elif positive and not negative:
            content_level = 3
        else:
            content_level = math.floor(sum(content_levels) / len(content_levels))
    else:
        content_level = 0

    if len(security_levels) > 0:
        positive = 3 in security_levels
        negative = 1 in security_levels

        if positive and negative:
            security_level = 2
        elif not positive and negative:
            security_level = 1
        elif positive and not negative:
            security_level = 3
        else:
            security_level = math.floor(sum(security_levels) / len(security_levels))
    else:
        security_level = 0

    learner_stats['levels']= {
        'auth': auth_level,
        'content': content_level,
        'security': security_level
    }

    return learner_stats


def _get_temporal_results(data, break_far_samples=True):

    max_gap_seconds = 240

    res_struct = {
        'date': [],
        'value': [],
        'error': []
    }

    last_date = None
    for point in data:
        if break_far_samples and (last_date is None or (point.date-last_date).total_seconds()>max_gap_seconds):
            res_struct['date'].append((point.date - timedelta(0,1)).__str__())
            res_struct['value'].append('NaN')
            res_struct['error'].append('')
        last_date = point.date
        res_struct['date'].append(point.date.__str__())
        res_struct['value'].append(round(float(point.value)*100))
        res_struct['error'].append(str(point.value))
    if break_far_samples and last_date is not None:
        res_struct['date'].append((last_date + timedelta(0, 1)).__str__())
        res_struct['value'].append('NaN')
        res_struct['error'].append('')

    return res_struct


def _get_audit_object(audit_string, audit=None):

    audit_obj = simplejson.loads(audit_string)

    if audit is None:
        return audit_obj

    audit['results']['frame_details'] += audit_obj['results']['frame_details']
    audit['results']['total_frames'] += audit_obj['results']['total_frames']
    audit['results']['valid_frames'] += audit_obj['results']['valid_frames']
    audit['results']['frame_codes'] += audit_obj['results']['frame_codes']
    audit['results']['error_frames'] += audit_obj['results']['error_frames']

    return audit

def _get_activity_audit(activity, instrument, tesla_id, audit=None):
    #inst_api = InstrumentAPI(app.config, logger, instrument)
    #audit_data = inst_api.get_activity_data(activity.vle_id, activity.activity_type, activity.activity_id, tesla_id)
    audit_data = tep_db.get_activity_audit(activity.vle_id, activity.activity_type, activity.activity_id, tesla_id, instrument.id)

    for a in audit_data:
        if a['finish'] is not None:
            audit = _get_audit_object(a['audit'], audit)

    return audit


def _get_course_audit(course, instrument, tesla_id):
    activities = tesla_db.courses.get_available_activities(course.id)

    audit = None
    for act in activities:
        audit = _get_activity_audit(act, instrument, tesla_id, audit)

    return audit

@reports.route('/course/<int:id>', methods=['GET'])
@reports.route('/course/<int:id>/<int:page>', methods=['GET'])
@reports.route('/course/<int:id>/<int:page>/<string:view>', methods=['GET'])
@login_required
@roles_required('Statistics')
def course_report(id, page=1, view='table'):
    # Verify the course
    course = tesla_db.courses.get_course(id)
    if course is None:
        return 404

    # Get filter parameters from request query parameters
    max_per_page = 20
    instrument_ids = None

    # Get the list of instruments that have some request for this course
    course_instruments = tesla_db.reports.get_course_instruments_with_requests(course.id)

    # Get course statistics for involved instruments
    context_statistics = {}
    for instrument in course_instruments:
        context_statistics[instrument.id] = {}
        context_statistics[instrument.id]['histogram'] = tesla_db.statistics.verification_course_results_histogram(course.id, instrument.id)
        context_statistics[instrument.id]['thresholds'] = tesla_db.instruments.get_instrument_thresholds(instrument.id)

    # Get a paginated list of learners that will be in the response
    learners = tesla_db.reports.get_course_learners_with_results(course.id, page=page, max_per_page=max_per_page,
                                                                   instrument_ids=instrument_ids)

    # Get the data for each learner
    results = schemas.ActivitySummaryPagination().dump(learners).data
    for learner_result in results['items']:
        tesla_id = learner_result['tesla_id']
        summary = tesla_db.courses.get_course_learner_summary(course.id, tesla_id)
        summary_json = schemas.LearnerInstrumentResults(many=True).dump(summary).data

        # Build indexed data to make easier the results visualization
        indexed_info = {}
        for inst in summary_json:
            indexed_info[inst['instrument_id']] = inst

        # Update the learner data on the paginated view
        learner_result.update({"instruments": indexed_info})

        # Add learner level statistics
        learner_result.update({"stats": _get_learner_instrument_stats(learner_result, context_statistics)})

    # Build the paginated iterator as a list, since items type is JSON.
    results['iter_pages'] = [p for p in learners.iter_pages(left_edge=1, left_current=2, right_current=3, right_edge=1)]

    return render_template('activity_report.html', pagination=results, endpoint='reports.course_report', view=view,
                           object=course, instruments=course_instruments)


@reports.route('/activity/<int:id>', methods=['GET'])
@reports.route('/activity/<int:id>/<int:page>', methods=['GET'])
@reports.route('/activity/<int:id>/<int:page>/<string:view>', methods=['GET'])
@login_required
@roles_required('Statistics')
def activity_report(id, page=1, view='table'):
    # Verify the activity
    activity = tesla_db.activities.get_activity(id)
    if activity is None:
        return 404

    # Get filter parameters from request query parameters
    max_per_page = 20
    instrument_ids = None

    # Get the list of instruments that have some request for this activity
    activity_instruments = tesla_db.reports.get_activity_instruments_with_requests(activity.id)

    # Get activity statistics for involved instruments
    context_statistics = {}
    for instrument in activity_instruments:
        context_statistics[instrument.id] = {}
        context_statistics[instrument.id]['histogram'] = tesla_db.statistics.verification_activity_results_histogram(
            activity.id, instrument.id)
        context_statistics[instrument.id]['thresholds'] = tesla_db.instruments.get_instrument_thresholds(instrument.id)

    # Get a paginated list of learners that will be in the response
    learners = tesla_db.reports.get_activity_learners_with_results(activity.id, page=page, max_per_page=max_per_page, instrument_ids=instrument_ids)

    # Get the data for each learner
    results = schemas.ActivitySummaryPagination().dump(learners).data
    for learner_result in results['items']:
        tesla_id = learner_result['tesla_id']
        summary = tesla_db.activities.get_activity_learner_summary(activity.id, tesla_id)
        summary_json = schemas.LearnerInstrumentResults(many=True).dump(summary).data

        # Build indexed data to make easier the results visualization
        indexed_info = {}
        for inst in summary_json:
            indexed_info[inst['instrument_id']] = inst

        # Update the learner data on the paginated view
        learner_result.update({"instruments": indexed_info})

        # Add learner level statistics
        learner_result.update({"stats": _get_learner_instrument_stats(learner_result, context_statistics)})

    # Build the paginated iterator as a list, since items type is JSON.
    results['iter_pages'] = [p for p in learners.iter_pages(left_edge=1, left_current=2, right_current=3, right_edge=1)]

    return render_template('activity_report.html', pagination=results, endpoint='reports.activity_report', view=view, object=activity, instruments=activity_instruments)


@reports.route('/course/<int:course_id>/learner/<uuid:tesla_id>', methods=['GET'])
@login_required
@roles_required('Statistics')
def course_learner_audit(course_id, tesla_id):

    tesla_id = str(tesla_id)
    # Verify the course
    course = tesla_db.courses.get_course(course_id)
    if course is None:
        return 404

    # Verify the learner
    learner = tesla_db.learners.get_learner(tesla_id)
    if learner is None:
        return 404

    # Get the list of instruments that have some request for this course
    course_instruments = tesla_db.reports.get_course_instruments_with_requests(course.id)

    # Get course statistics for involved instruments
    context_statistics = {}
    for instrument in course_instruments:
        context_statistics[instrument.id] = {}
        context_statistics[instrument.id]['histogram'] = tesla_db.statistics.verification_course_results_histogram(
            course.id, instrument.id)
        context_statistics[instrument.id]['thresholds'] = tesla_db.instruments.get_instrument_thresholds(instrument.id)
        context_statistics[instrument.id]['temporal'] = _get_temporal_results(tesla_db.reports.get_course_learner_temporal_results(course.id, tesla_id, instrument.id))
        context_statistics[instrument.id]['aronym'] = instrument.acronym

    summary = tesla_db.courses.get_course_learner_summary(course.id, tesla_id)
    summary_json = schemas.LearnerInstrumentResults(many=True).dump(summary).data

    # Build indexed data to make easier the results visualization
    indexed_info = {}
    for inst in summary_json:
        indexed_info[inst['instrument_id']] = inst

    # Update the learner data on the paginated view
    learner_result = {
        "tesla_id" : tesla_id,
        "instruments": indexed_info,
        "failed_requests": _get_temporal_results(tesla_db.reports.get_course_learner_temporal_failed_requests(course.id, tesla_id), break_far_samples=False)
    }

    # Add learner level statistics
    learner_result.update({"stats": _get_learner_instrument_stats(learner_result, context_statistics)})

    return render_template('learner_audit.html', learner=learner_result, object=course, instruments=course_instruments, context_statistics=context_statistics, tesla_id=tesla_id)


@reports.route('/activity/<int:activity_id>/learner/<uuid:tesla_id>', methods=['GET'])
@login_required
@roles_required('Statistics')
def activity_learner_audit(activity_id, tesla_id):

    tesla_id = str(tesla_id)

    # Verify the activity
    activity = tesla_db.activities.get_activity(activity_id)
    if activity is None:
        return 404

    # Verify the learner
    learner = tesla_db.learners.get_learner(tesla_id)
    if learner is None:
        return 404

    # Get the list of instruments that have some request for this activity
    activity_instruments = tesla_db.reports.get_activity_instruments_with_requests(activity.id)

    # Get activity statistics for involved instruments
    context_statistics = {}
    for instrument in activity_instruments:
        context_statistics[instrument.id] = {}
        context_statistics[instrument.id][
            'histogram'] = tesla_db.statistics.verification_activity_results_histogram(
            activity.id, instrument.id)
        context_statistics[instrument.id]['thresholds'] = tesla_db.instruments.get_instrument_thresholds(
            instrument.id)
        context_statistics[instrument.id]['temporal'] = _get_temporal_results(
            tesla_db.reports.get_activity_learner_temporal_results(activity.id, tesla_id, instrument.id))
        context_statistics[instrument.id]['aronym'] = instrument.acronym

    summary = tesla_db.activities.get_activity_learner_summary(activity.id, tesla_id)
    summary_json = schemas.LearnerInstrumentResults(many=True).dump(summary).data

    # Build indexed data to make easier the results visualization
    indexed_info = {}
    for inst in summary_json:
        indexed_info[inst['instrument_id']] = inst

    # Update the learner data on the paginated view
    learner_result = {
        "tesla_id": tesla_id,
        "instruments": indexed_info,
        "failed_requests": _get_temporal_results(
            tesla_db.reports.get_activity_learner_temporal_failed_requests(activity.id, tesla_id), break_far_samples=False)
    }

    # Add learner level statistics
    learner_result.update({"stats": _get_learner_instrument_stats(learner_result, context_statistics)})

    return render_template('learner_audit.html', learner = learner_result, object=activity, instruments=activity_instruments, context_statistics=context_statistics, tesla_id=tesla_id)


@reports.route('/activity/<int:activity_id>/learner/<uuid:tesla_id>/<int:instrument_id>', methods=['GET'])
@login_required
@roles_required('Statistics')
def activity_learner_audit_instrument(activity_id, tesla_id, instrument_id):

    tesla_id = str(tesla_id)

    # Verify the activity
    activity = tesla_db.activities.get_activity(activity_id)
    if activity is None:
        return 404

    # Verify the learner
    learner = tesla_db.learners.get_learner(tesla_id)
    if learner is None:
        return 404

    # Verify the instrument
    instrument = tesla_db.instruments.get_instrument_by_id(instrument_id)
    if instrument is None:
        return 404

    # Check that the instrument have audit possibilities
    if instrument_id not in [1]:
        return 405

    return render_template('learner_audit_instrument.html', object=activity, tesla_id=tesla_id, instrument=instrument)


@reports.route('/course/<int:course_id>/learner/<uuid:tesla_id>/<int:instrument_id>', methods=['GET'])
@login_required
@roles_required('Statistics')
def course_learner_audit_instrument(course_id, tesla_id, instrument_id):

    tesla_id = str(tesla_id)

    # Verify the course
    course = tesla_db.courses.get_course(course_id)
    if course is None:
        return 404

    # Verify the learner
    learner = tesla_db.learners.get_learner(tesla_id)
    if learner is None:
        return 404

    # Verify the instrument
    instrument = tesla_db.instruments.get_instrument_by_id(instrument_id)
    if instrument is None:
        return 404

    # Check that the instrument have audit possibilities
    if instrument_id not in [1]:
        return 405

    return render_template('learner_audit_instrument.html', object=course, tesla_id=tesla_id, instrument=instrument)




@reports.route('/course/audit/<int:course_id>/<uuid:tesla_id>/<int:instrument_id>', methods=['GET'])
@login_required
@roles_required('Statistics')
def get_course_audit_ajax(course_id, tesla_id, instrument_id):
    tesla_id = str(tesla_id)

    # Verify the course
    course = tesla_db.courses.get_course(course_id)
    if course is None:
        return 404

    # Verify the learner
    learner = tesla_db.learners.get_learner(tesla_id)
    if learner is None:
        return 404

    # Verify the instrument
    instrument = tesla_db.instruments.get_instrument_by_id(instrument_id)
    if instrument is None:
        return 404

    # Check that the instrument have audit possibilities
    if instrument_id not in [1]:
        return 405

    audit_json = _get_course_audit(course, instrument, tesla_id)

    if audit_json is None:
        audit_json = {
            'results': {
                'frame_details': [],
                'total_frames': 0,
                'valid_frames': 0,
                'frame_codes':[],
                'error_frames':0
            },
            'enrollment_user_faces': [],
            'version': 'TFR 1.0'
        }

    return jsonify(audit_json)


@reports.route('/activity/audit/<int:activity_id>/<uuid:tesla_id>/<int:instrument_id>', methods=['GET'])
@login_required
@roles_required('Statistics')
def get_activity_audit_ajax(activity_id, tesla_id, instrument_id):

    tesla_id = str(tesla_id)

    # Verify the activity
    activity = tesla_db.activities.get_activity(activity_id)
    if activity is None:
        return 404

    # Verify the learner
    learner = tesla_db.learners.get_learner(tesla_id)
    if learner is None:
        return 404

    # Verify the instrument
    instrument = tesla_db.instruments.get_instrument_by_id(instrument_id)
    if instrument is None:
        return 404

    # Check that the instrument have audit possibilities
    if instrument_id not in [1]:
        return 405

    audit_json = _get_activity_audit(activity, instrument, tesla_id)

    if audit_json is None:
        audit_json = {
            'results': {
                'frame_details': [],
                'total_frames': 0,
                'valid_frames': 0,
                'frame_codes':[],
                'error_frames':0
            },
            'enrollment_user_faces': [],
            'version': 'TFR 1.0'
        }

    return jsonify(audit_json)
