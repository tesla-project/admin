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

function actions_format_selected(value, row, index, field) {
    html = ' <button class="btn btn-sm btn-danger btn-delete-activity" data-entity-id="'+row.id+'"><i class="fa fa-trash"></i></button>';

    return html;
}

$(function () {
    $("body").on('click', '.btn-delete-activity', function(event){
        var activity_id = $(event.currentTarget).data('entity-id');
        $.ajax(Flask.url_for("data.delete_activity", {'activity_id': activity_id}), {
            method: 'DELETE'
        }).done(function(data) {
            window.location.href = Flask.url_for("data.activity");
        }).fail(function() {

        });
    });
});