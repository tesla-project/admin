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

function show_vle_data(id) {
    $('.vle-details').show();
    $("#id").val(id);
    if (id < 0) {
        // Creating a new vle
        $('.vle-details').hide();
        $(".detail-form-loading").hide();
        $(".vle-form").hide();
    } else {
        // Modify existing course
        $("#delete").show();
        $(".vle-form").hide();
        $(".detail-form-loading").show();
        $.ajax(Flask.url_for("system.get_vle_data", {'id': id}), {
            method: 'GET'
        }).done(function(data) {
            $("#id").val(data['id']);
            $("#name").val(data['name']);
            $("#vle_id").val(data['vle_id']);
            $("#token").val(data['token']);
            $("#url").val(data['url']);
            $(".detail-form-loading").hide();
            $(".vle-form").show();
        }).fail(function() {
            $('.vle-details').hide();
            $(".detail-form-loading").hide();
            $(".vle-form").hide();
        });
    }
}

$(function () {
    $("#vles").on('change', function() {
        show_vle_data($(this).val());
    });
    if($("#id").val()>0) {
        $("#vles").val($("#id").val());
        show_vle_data($("#id").val());
    }
});