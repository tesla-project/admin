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

$(".btn-environment-edit").click(function(e){
    e.preventDefault();
    e.stopPropagation();

    var entity_id = $(this).data('id');
    var type = $(this).data('type');

    $("#modal_environment").modal('hide');
    $("#modal_environment").html('');

    $("#modal_environment").load( Flask.url_for("system.management_environment", {"id": entity_id, "type": type}), null, function(){
        $("#modal_environment").modal('show');
    }, function(){
        console.log('errror');
    });


});

$("body").on("click", ".btn-environment-submit", function(){
    if ($("#form_environment").valid()) {
        $("#form_environment").submit();
    }
});