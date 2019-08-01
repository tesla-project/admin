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

from flask import Blueprint, jsonify, url_for, render_template, request, redirect, flash
from flask_security import roles_required, login_required
from tesla_admin import tesla_db, get_locale
from tesla_models import models
from tesla_admin.blueprints.users.forms import UserForm

users = Blueprint('users', __name__, template_folder='templates', static_folder='static')


@users.route('/', methods=['GET'])
@login_required
@roles_required('Admin')
def index():
    user_count = tesla_db.users.get_user_count()

    return render_template('index.html', page = 'users.index', user_count=user_count)


@users.route('/list_ajax', methods=['GET'])
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

    list_users = tesla_db.users.get_users(q=q, limit=limit, offset=offset, order=order, sort=sort)
    total_users = tesla_db.users.count_users(q=q)

    users_data = models.users_schema.dump(list_users)

    return_data = {}
    return_data['total'] = total_users
    return_data['rows'] = users_data[0]

    return jsonify(return_data), 200


@users.route('/user_delete', methods=['GET'])
@login_required
@roles_required('Admin')
def user_delete():
    id = request.args.get('id')
    if tesla_db.users.user_delete(id) is True:
        flash('Data deleted', 'success')
    else:
        flash('Data not deleted', 'error')


    return redirect(url_for('users.index'))

@users.route('/user_addedit', methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def user_addedit(id=0):
    id = int(request.args.get('id'))
    user_obj = tesla_db.users.get_user(id)

    form = UserForm(obj=user_obj)

    has_errors = True
    if form.validate_on_submit():
        tesla_db.users.user_addedit(id, form)
        flash('Data saved', 'success')
        return redirect(url_for('users.index'))
    else:
        return render_template('user_addedit.html', form=form, has_errors=has_errors, id=id)


@users.route('/roles', methods=['GET'])
@login_required
@roles_required('Admin')
def roles():
    return render_template('roles.html', page = 'users.roles')
