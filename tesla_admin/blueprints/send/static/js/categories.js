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

function show_category_data(id) {
    $('.category-details').show();
    $("#id").val(id);
    if (id < 0) {
        // Creating a new category
        $("#form_category")[0].reset();
        $(".is-invalid").removeClass("is-invalid");
        $(".category-form-loading").hide();
        $(".category-form").show();
    } else {
        // Modify existing category
        $(".category-form").hide();
        $(".category-form-loading").show();
        $.ajax(Flask.url_for("send.get_category_data", {'id': id}), {
            method: 'GET'
        }).done(function(data) {
            $("#id").val(data['id']);
            $("#description").val(data['description']);
            var options = data['data']['options'];
            var instruments = data['data']['instruments'];
            $.each($('input[name="options"]'), function() {
                if (options.indexOf($(this).val()) >= 0) {
                    $(this).prop('checked', true);
                }
            });
            $.each($('input[name="instruments"]'), function() {
                if (instruments.indexOf(parseInt($(this).val())) >= 0) {
                    $(this).prop('checked', true);
                }
            });
            $(".category-form-loading").hide();
            $(".category-form").show();
        }).fail(function() {
            $('.category-details').hide();
            $(".category-form-loading").hide();
            $(".category-form").hide();
        });
    }
}

$(function () {
    $(".new_category").click(function(){
        show_category_data(-1);
    });
    $("#categories").on('change', function() {
        show_category_data($(this).val());
    });
});