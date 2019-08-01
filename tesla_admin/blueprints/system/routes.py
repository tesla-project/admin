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

from flask import Blueprint, jsonify, url_for, render_template, request, flash, redirect, Response
from tesla_admin.decorators import certificate_required
from tesla_admin import logger, tesla_db
from tesla_admin.helpers import api_response
from tesla_admin.errors import TESLA_API_STATUS_CODE
import simplejson as json
from tesla_admin.git_config import get_config_repository
from flask_security import roles_required, login_required
from .forms import VLETokenForm
from tesla_admin.env_classify import EnvClassify

system = Blueprint('system', __name__, template_folder='templates', static_folder='static')


@system.route('/management', methods=['GET'])
@login_required
@roles_required('Admin')
def configuration():
    instruments = tesla_db.instruments.get_instruments()
    return_instruments = []
    for instrument in instruments:
        aux = {}
        aux['id'] = instrument.id
        aux['name'] = instrument.name

        aux['thresholds'] = {}
        aux['thresholds']['low'] = ''
        aux['thresholds']['medium'] = ''
        aux['thresholds']['high'] = ''
        aux['thresholds']['audit_data'] = ''
        thresholds = tesla_db.instruments.get_instrument_thresholds(instrument.id)

        if thresholds is not None:
            aux['thresholds']['low'] = thresholds.low
            aux['thresholds']['medium'] = thresholds.medium
            aux['thresholds']['high'] = thresholds.high
            aux['thresholds']['audit_level'] = thresholds.audit_level

        return_instruments.append(aux)

    services = get_config_repository().get_service_list()
    modules = get_config_repository().get_module_list()

    return render_template('configuration.html', page='system.configuration', instruments=return_instruments,
                           services=services, modules=modules)


@system.route('/management/instrument/<int:id>', methods=['POST'])
@login_required
@roles_required('Admin')
def management_instrument(id):
    low = request.form.get('threshold_low')
    medium = request.form.get('threshold_medium')
    high = request.form.get('threshold_high')
    audit_level = request.form.get('threshold_audit_level')

    result = tesla_db.instruments.create_or_update_instrument_thresholds(instrument_id=id, low=low, medium=medium,
                                                                         high=high, audit_level=audit_level)

    if result is None:
        flash('Data not saved', 'error')
    else:
        flash('Data saved', 'success')

    return redirect(url_for('system.configuration'))


@system.route('/management/environment/<string:type>/<string:id>', methods=['GET'])
@login_required
@roles_required('Admin')
def management_environment(type, id):
    permitted_types = ["module", "service"]

    if type not in permitted_types:
        return api_response(TESLA_API_STATUS_CODE.BAD_REQUEST, data={"message": "invalid type"}, http_code=400)


    config_from_service_keys = []
    all_config = {
        "dependencies": {},
        "config": []
    }
    config_icons = {}

    if type == 'module':
        config_obj = get_config_repository().get_module_config(id)

        services_dependencies = []

        if config_obj.get_module_dependencies() is not None:
            services_dependencies = config_obj.get_module_dependencies()['services']

        for service_dependency in services_dependencies:
            configs_service_dependency = config_obj.get_service_config(service_dependency)
            if service_dependency not in all_config['dependencies'].keys():
                all_config['dependencies'][service_dependency] = []
                config_icons[service_dependency] = EnvClassify().get_icon(type="service", service_name=service_dependency)

            for (config_service_dependency_key, config_service_dependency_value) in configs_service_dependency.items():
                config_from_service_keys.append(config_service_dependency_key)

                aux = EnvClassify().get_info(type="service", service_name=service_dependency, key=config_service_dependency_key)
                aux['value'] = config_service_dependency_value

                all_config['dependencies'][service_dependency].append(aux)


    else:
        config_obj = get_config_repository().get_service_config(id)

    configs = config_obj.get_config()

    for (key, value) in configs.items():
        if key not in config_from_service_keys:
            aux = EnvClassify().get_info(type=type, service_name=id, key=key)
            aux['value'] = value
            all_config['config'].append(aux)

    return render_template('configuration/modal_environment.html', all_config=all_config, config_icons=config_icons, type=type, id=id)


@system.route('/management/environment/<string:type>/<string:id>', methods=['POST'])
@login_required
@roles_required('Admin')
def management_environment_save(type, id):
    permitted_types = ["module", "service"]

    if type not in permitted_types:
        return api_response(TESLA_API_STATUS_CODE.BAD_REQUEST, data={"message": "invalid type"}, http_code=400)


    config_from_service_keys = []

    if type == 'module':
        config_obj = get_config_repository().get_module_config(id)

        services_dependencies = config_obj.get_module_dependencies()['services']

        for service_dependency in services_dependencies:
            service_dependency_aux = {}
            configs_service_dependency = config_obj.get_service_config(service_dependency)

            for (config_service_dependency_key, config_service_dependency_value) in configs_service_dependency.items():
                config_from_service_keys.append(config_service_dependency_key)

                value = request.form.get('dependencies['+str(service_dependency)+"]["+str(config_service_dependency_key)+"]")

                service_dependency_aux[config_service_dependency_key] = value

            config_obj.set_service_config(service_dependency, service_dependency_aux)

    else:
        config_obj = get_config_repository().get_service_config(id)

    configs = config_obj.get_config()

    for (key, value) in configs.items():
        if key not in config_from_service_keys:
            value = request.form.get("general["+str(key)+"]")
            config_obj.set_value(key, value)

    flash('Data saved', 'success')

    return redirect(url_for('system.configuration'))


@system.route('/monitoring', methods=['GET'])
@login_required
@roles_required('Admin')
def monitoring():
    instruments = tesla_db.instruments.get_instruments()
    return render_template('monitoring.html', page='system.monitoring', instruments=instruments)


@system.route('/instrument_status', methods=['GET'])
@login_required
@roles_required('Admin')
def instrument_status():
    instruments = tesla_db.instruments.get_instrument_status()
    ret_val = []
    for inst in instruments:
        service_info = None
        if inst.InstrumentQueue.service_info is not None:
            service_info = json.loads(inst.InstrumentQueue.service_info)
        updated = inst.InstrumentQueue.created
        if inst.InstrumentQueue.updated is not None:
            updated = inst.InstrumentQueue.updated
        ret_val.append({
            'acronym': inst.Instrument.acronym,
            'pending': inst.InstrumentQueue.pending_tasks,
            'd1': inst.InstrumentQueue.tendency1,
            'd2': inst.InstrumentQueue.tendency2,
            'workers': inst.InstrumentQueue.consumers,
            'active': inst.Instrument.active,
            'service': inst.InstrumentQueue.service,
            'service_info': service_info,
            'updated': updated
        })
    return api_response(TESLA_API_STATUS_CODE.SUCCESS, {'status': ret_val})


@system.route('/vle', methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def vle():
    form = VLETokenForm()

    has_errors = True
    if form.validate_on_submit():
        if form.data.get('submit'):
            tesla_db.vle.update_vle_access(id=form.data.get('id'), token=form.data.get('token'), url=form.data.get('url'))
            has_errors = False

        if form.data.get('delete'):
            if tesla_db.vle.update_vle_access(form.data["id"]):
                return redirect(url_for('system.vle'))

    if request.method == "GET":
        has_errors = False

    conf_vles = tesla_db.vle.get_vles()

    return render_template('vle_token.html', page='system.vle', form=form, conf_vles=conf_vles, has_errors=has_errors)


@system.route('/vle/<int:id>', methods=['GET'])
@login_required
@roles_required('Admin')
def get_vle_data(id):
    vle = tesla_db.vle.get_vle(id)
    if vle is None:
        return api_response(TESLA_API_STATUS_CODE.REQUEST_NOT_FOUND, http_code=404)

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, {'id': vle.id, 'vle_id': vle.vle_id,
                                                        'url': vle.url, 'token': vle.token, 'name': vle.name})