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
from .forms import CategoryForm
from tesla_models.database.utils import decode_data
from flask_security import roles_required, login_required

send = Blueprint('send', __name__, template_folder='templates', static_folder='static')

@send.route('/learners', methods=['GET'])
@login_required
@roles_required('Admin')
def learners():
    form = CategoryForm()

    categories = tesla_db.learners.get_send_categories()

    return render_template('learners.html', page = 'send.learners', form=form, categories=categories)


@send.route('/learner/categories/<string:tesla_id>', methods=["GET"])
@login_required
@roles_required('Admin')
def get_learner_categories(tesla_id):

    categories = tesla_db.learners.get_send_user(tesla_id)

    instruments = set()
    options = set()
    cat = []
    for c in categories:
        data = decode_data(c.data)
        c.data = data
        instruments.update(data['instruments'])
        options.update(data['options'])
        cat.append(c.id)

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, {"categories": cat, "instruments": list(instruments), "options": list(options)})


@send.route('/learner/categories/<string:tesla_id>', methods=["POST"])
@login_required
@roles_required('Admin')
def set_learner_categories(tesla_id):

    # Update assigned categories
    new_cats = request.get_json()

    if new_cats is not None:
        tesla_db.learners.update_learner_send_categories(tesla_id, new_cats['categories'])

    return get_learner_categories(tesla_id)


@send.route('/categories', methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def categories():
    form = CategoryForm()

    has_errors = True
    if form.validate_on_submit():
        data = {'options': form.data.get('options'), 'instruments': [int(i) for i in form.data.get('instruments')]}
        if form.data["id"] < 0:
            tesla_db.learners.create_send_category(description=form.data.get('description'), data=data)
        else:
            tesla_db.learners.update_send_category(id=form.data.get('id'), description=form.data.get('description'), data=data)
        has_errors = False

    if request.method == "GET":
        has_errors = False

    categories = tesla_db.learners.get_send_categories()

    return render_template('categories.html', page='send.categories', form=form, categories=categories, has_errors=has_errors)


@send.route('/category/<int:id>', methods=['GET'])
@login_required
@roles_required('Admin')
def get_category_data(id):
    category = tesla_db.learners.get_send_category(id)
    if category is None:
        api_response(TESLA_API_STATUS_CODE.REQUEST_NOT_FOUND, http_code=404)
    data = decode_data(category.data)

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, {'id': category.id, 'description': category.description,
                                                        'data': data})
