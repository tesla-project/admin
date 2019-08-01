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

function actions_format_available(value, row, index, field) {
    html = '<button class="btn btn-sm btn-success btn-add-activity" type="button" data-entity-id="'+row.id+'"><i class="fa fa-plus-square"></i></button>';

    return html;
}

function actions_format_selected(value, row, index, field) {
    html = ' <button class="btn btn-sm btn-danger btn-delete-activity" data-entity-id="'+row.id+'"><i class="fa fa-trash"></i></button>';

    return html;
}

function show_course_data(id) {
    $('.course-details').show();
    $('#table_available_activities').bootstrapTable('removeAll');
    $('#table_selected_activities').bootstrapTable('removeAll');
    $("#id").val(id);
    if (id < 0) {
        // Creating a new course
        $("#delete").hide();
        $("#form_course")[0].reset();
        $("#parent").val(-1);
        $(".is-invalid").removeClass("is-invalid");
        $(".course-form-loading").hide();
        $(".course-form").show();
        $('.course-activities').hide();
        $('#parent').select2({width: 'resolve', theme: "bootstrap4"});
    } else {
        // Modify existing course
        $("#delete").show();
        $(".course-form").hide();
        $(".course-form-loading").show();
        $.ajax(Flask.url_for("data.get_course_data", {'id': id}), {
            method: 'GET'
        }).done(function(data) {
            $("#id").val(data['id']);
            $("#parent").val(data['parent_id']);
            $("#code").val(data['code']);
            $("#description").val(data['description']);
            if(data['start']){
                $("#start").val(moment(data['start']).format('YYYY-MM-DD'));
            } else {
                $("#start").val(null);
            }
            if(data['end']){
                $("#end").val(moment(data['end']).format('YYYY-MM-DD'));
            } else {
                $("#end").val(null);
            }
            $("#vle_id").val(data['vle_id']);
            $("#vle_course_id").val(data['vle_course_id']);
            $(".course-form-loading").hide();
            $(".course-form").show();
            $('#parent').select2({width: 'resolve', theme: "bootstrap4"});
        }).fail(function() {
            $('.course-details').hide();
            $(".course-form-loading").hide();
            $(".course-form").hide();
            $('#parent').select2({width: 'resolve', theme: "bootstrap4"});
        });
        $('.course-activities').show();
        $('#table_available_activities').bootstrapTable('refresh', {url: Flask.url_for('data.list_available_activities_ajax', {id: id})});
        $('#table_selected_activities').bootstrapTable('refresh', {url: Flask.url_for('data.list_selected_activities_ajax', {id: id})});
    }
}

$(function () {
    $(".new_course").click(function(){
        show_course_data(-1);
    });
    $("#courses").on('change', function() {
        show_course_data($(this).val());
    });
    $("body").on('click', '.btn-add-activity', function(event){
        var course_id = $("#id").val();
        var activity_id = $(event.currentTarget).data('entity-id');
        $.ajax(Flask.url_for("data.course_activity", {'course_id': course_id, 'activity_id': activity_id}), {
            method: 'POST'
        }).done(function(data) {
            $('#table_available_activities').bootstrapTable('refresh');
            $('#table_selected_activities').bootstrapTable('refresh');
        }).fail(function() {

        });
    });

    $("body").on('click', '.btn-delete-activity', function(event){
        var course_id = $("#id").val();
        var activity_id = $(event.currentTarget).data('entity-id');
        $.ajax(Flask.url_for("data.course_activity", {'course_id': course_id, 'activity_id': activity_id}), {
            method: 'DELETE'
        }).done(function(data) {
            $('#table_available_activities').bootstrapTable('refresh');
            $('#table_selected_activities').bootstrapTable('refresh');
        }).fail(function() {

        });
    });

    if($("#id").val()>0) {
        $("#courses").val($("#id").val());
        show_course_data($("#id").val());
    }

    $('#parent').select2({width: 'resolve', theme: "bootstrap4"});
});