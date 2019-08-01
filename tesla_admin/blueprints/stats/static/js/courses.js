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

function date_formatter(value, row, index, field) {
    if (value == null) return '';
    return moment(value).format("L");
}

function result_plot(value, row, index, field) {
    html = [];
    //html.push('<div class="inline-results"><span class="sparkboxplot">');
    html.push('<div class="inline-results"><span class="sparkbarplot">');
    html.push(value.join(', '));
    html.push('</span></div>');
    return html.join('')
}

function update_course_stats(course_id, stats){
    $('#current_course_num_learners').text(stats['num_learners']);
    $('#current_learner_num_activities').text(stats['num_activities']);
    $('#table_instrument_data').bootstrapTable('refresh', {'url': Flask.url_for('stats.list_course_instruments_ajax', {'course_id': course_id})});
    $('.course-info').hide();
    $('.course-info-data').show();
}

function show_course_data(course_id) {
    $('.course-info').hide();
    $('.course-info-loading').show();
    $('#table_instrument_data').bootstrapTable('removeAll');

    $.ajax(Flask.url_for("stats.course_stats", {"course_id": course_id}), {
        method: 'GET'
    }).done(function(stats) {
        update_course_stats(course_id, stats['stats']);
    }).fail(function() {
        $('.course-info').hide();
        $('.course-info-data').show();
    }).always(function() {

    });
}

$(function () {
    $('#table_instrument_data').bootstrapTable();
    $('#table_instrument_data').on('post-body.bs.table', function (e, data) {
        //$('.sparkboxplot').sparkline('html', { type: 'box', minValue: 0, maxValue: 1, "height": "1.3em"});
        $('.sparkbarplot').sparkline('html', { type: 'bar', minValue: 0, maxValue: 1, "height": "1.3em"});
    });
    $('#table_courses').on('dbl-click-row.bs.table', function (e, row, $element, field) {
        var course_id = row['id'];
        show_course_data(course_id);
    });

    var tree = $('#courses_tree').tree({
        primaryKey: 'id',
        uiLibrary: 'bootstrap4',
        iconsLibrary: 'fontawesome',
        border: true,
        lazyLoading: true,
        parentId: 'parent_id',
        dataSource: Flask.url_for("stats.get_course_tree")
    });

    tree.on('select', function (e, node, id) {
        show_course_data(id);
    });
    tree.on('unselect', function (e, node, id) {
        $('.course-info-data').hide();
        $('.course-info-nodata').show();
    });
});