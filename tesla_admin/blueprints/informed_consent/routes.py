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

from flask import Blueprint, jsonify, url_for, render_template, request, flash, redirect, make_response
from tesla_admin.decorators import certificate_required
from tesla_admin import logger
from tesla_admin.helpers import api_response
from tesla_admin.errors import TESLA_API_STATUS_CODE
from flask_security import roles_required, login_required
from tesla_admin import tesla_db, get_locale
from tesla_models import models
from tesla_admin.blueprints.informed_consent.forms import InformedConsentForm
from tesla_models.errors import not_found

informed_consent = Blueprint('informed_consent', __name__, template_folder='templates', static_folder='static')

@informed_consent.route('/', methods=['GET'])
@login_required
@roles_required('Admin')
def index():
    return render_template('versions.html', page='informed_consent.versions')


@informed_consent.route('/list_ajax', methods=['GET'])
@login_required
@roles_required('Admin')
def list_ajax():
    q = None
    limit = None
    offset = None

    q = request.args.get('search')
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    sort = request.args.get('sort')
    order = request.args.get('order')

    list_entity = tesla_db.informed_consent.get_informed_consents(q=q, limit=limit, offset=offset, order=order, sort=sort)
    total = tesla_db.informed_consent.count_informed_consents(q=q)

    data = models.informed_consents_schema.dump(list_entity)

    return_data = {}
    return_data['total'] = total
    return_data['rows'] = data [0]

    return jsonify(return_data), 200

@informed_consent.route('/informed_consent_addedit', methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def informed_consent_addedit(id=0):
    id = int(request.args.get('id'))
    obj = tesla_db.informed_consent.get_informed_consent(id)

    form = InformedConsentForm(obj=obj)

    has_errors = True
    if form.validate_on_submit():
        tesla_db.informed_consent.informed_consent_addedit(id, form)
        flash('Data saved', 'success')
        return redirect(url_for('informed_consent.index'))
    else:
        return render_template('informed_consent_addedit.html', form=form, has_errors=has_errors, id=id)


@informed_consent.route('/informed_consent_documents_addedit', methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def informed_consent_documents_addedit(id=0):
    id = int(request.args.get('id'))
    obj = tesla_db.informed_consent.get_informed_consent(id)

    form = InformedConsentForm(obj=obj)

    has_errors = True
    if form.validate_on_submit():
        tesla_db.informed_consent.informed_consent_addedit(id, form)
        flash('Data saved', 'success')
        return redirect(url_for('informed_consent.index'))
    else:
        return render_template('informed_consent_addedit.html', form=form, has_errors=has_errors, id=id)

@informed_consent.route('/informed_consent_document_addedit', methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def informed_consent_document_addedit(id=0):
    languages = {
        'en': 'English',
        'es': 'Spanish',
        'ca': 'Catalan',
        'fr': 'French',
        'nl': 'Dutch',
        'de': 'German',
        'fi': 'Finnish',
        'bg': 'Bulgar',
        'tr': 'Turkish'
    }
    sorted_languages = sorted(languages)

    id = int(request.args.get('id'))
    objs = tesla_db.informed_consent.get_informed_consent_documents(id)
    print(objs)
    has_errors = True

    if request.form.get('documents_sent') == 'yes':

        for language in sorted_languages:
            html = request.form.get('html_'+str(language))
            pdf = request.files.get('pdf_'+str(language))

            if pdf is not None:
                pdf = pdf.read()

            tesla_db.informed_consent.informed_consent_document_addedit(id, language, html, pdf)

        return redirect(url_for('informed_consent.index'))
        '''
        if form.validate_on_submit():
            tesla_db.informed_consent.informed_consent_addedit(id, form)
            flash('Data saved', 'success')
            return redirect(url_for('informed_consent.versions'))
        '''
    else:
        return render_template('informed_consent_document_addedit.html', documents=objs, id=id, languages=languages,
                               sorted_languages=sorted_languages)


@informed_consent.route('/document_pdf_download/<int:consent_id>/<string:language>', methods=['GET'])
@login_required
@roles_required('Admin')
def document_pdf_download(consent_id, language):
    document = tesla_db.informed_consent.get_informed_consent_document(consent_id, language)
    if document.pdf:
        binary_pdf = document.pdf
        response = make_response(binary_pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=document_'+language+'.pdf'

        return response

    else:
        return not_found()
