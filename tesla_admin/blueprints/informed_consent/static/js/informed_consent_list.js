
/*
 * TeSLA Admin
 * Copyright (C) 2019 Universitat Oberta de Catalunya
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

function valid_format(value, row, index, field) {
    return moment(value).format('YYYY-MM-DD');
}

function actions_format(value, row, index, field) {
    html = '<button class="btn btn-sm btn-success btn-addedit" type="button" data-entity-id="'+row.id+'"><i class="fa fa-edit"></i></button>&nbsp;&nbsp;';
    html = html+'<button class="btn btn-sm btn-warning btn-document-addedit" type="button" data-entity-id="'+row.id+'"><i class="fa fa-file"></i></button>';

    return html;
}

$("body").on('click', '.btn-addedit', function(event){
    var id = $(event.currentTarget).data('entity-id');
    $("#entity_addedit .modal-content").html('');

    $("#entity_addedit .modal-content").load(Flask.url_for("informed_consent.informed_consent_addedit", {"id": id}), function() {
        $("#entity_addedit").modal('show');
    });
});

$("body").on('click', '.btn-document-addedit', function(event){
    var id = $(event.currentTarget).data('entity-id');
    $("#entity_addedit .modal-content").html('');

    $("#entity_addedit .modal-content").load(Flask.url_for("informed_consent.informed_consent_document_addedit", {"id": id}), function() {
        $("#entity_addedit").modal('show');
    });
});