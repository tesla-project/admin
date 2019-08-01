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
    html.push('<div class="inline-results"><span class="sparkbarplot">');
    html.push(value.join(', '));
    html.push('</span></div>');
    return html.join('')
}

function update_activity_stats(id, stats, type){
    $('#current_activity_num_learners').text(stats['num_learners']);
    $('#current_activity_num_instruments').text(stats['num_instruments']);
    if (type == 'activity') {
        $('#table_instrument_data').bootstrapTable('refresh', {'url': Flask.url_for('stats.list_activity_instruments_ajax', {'activity_id': id})});
    } else {
        $('#table_instrument_data').bootstrapTable('refresh', {'url': Flask.url_for('stats.list_course_instruments_ajax', {'course_id': id})});
    }
    $('.activity-info').hide();
    $('.activity-info-data').show();
}

function show_activity_data(id, type) {
    $('.activity-info').hide();
    $('.activity-info-loading').show();
    $('#table_instrument_data').bootstrapTable('removeAll');

    if (type == 'activity') {
        url = Flask.url_for("stats.activity_stats", {"activity_id": id});
        $('#show_report').attr('href', Flask.url_for("reports.activity_report", {"id": id}));
    } else {
        url = Flask.url_for("stats.course_stats", {"course_id": id});
        $('#show_report').attr('href', Flask.url_for("reports.course_report", {"id": id}));
    }

    $.ajax(url, {
        method: 'GET'
    }).done(function(stats) {
        update_activity_stats(id, stats['stats'], type);
    }).fail(function() {
        $('.activity-info').hide();
        $('.activity-info-data').show();
    }).always(function() {

    });
}

$(function () {
    $('#table_instrument_data').bootstrapTable();
    $('#table_instrument_data').on('post-body.bs.table', function (e, data) {
        $('.sparkbarplot').sparkline('html', { type: 'bar', minValue: 0, maxValue: 1, "height": "1.3em"});
    });

    var tree = $('#activities_tree').tree({
        primaryKey: 'id',
        uiLibrary: 'bootstrap4',
        iconsLibrary: 'fontawesome',
        border: true,
        lazyLoading: true,
        parentId: 'parent_id',
        dataSource: Flask.url_for("stats.get_activity_tree")
    });

    tree.on('select', function (e, node, id) {
        var data = tree.getDataById(id);
        show_activity_data(id, data['type']);
    });
    tree.on('unselect', function (e, node, id) {
        $('.activity-info-data').hide();
        $('.activity-info-nodata').show();
    });
});