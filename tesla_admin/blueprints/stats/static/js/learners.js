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

function result_plot(value, row, index, field) {
    html = [];
    //html.push('<div class="inline-results"><span class="sparkboxplot">');
    html.push('<div class="inline-results"><span class="sparkbarplot">');
    html.push(value.join(', '));
    html.push('</span></div>');
    return html.join('')
}

function update_learner_data(data) {
    $('#current_learner_num_courses').text(data['courses']);
    $('#current_learner_num_activities').text(data['activities']);
    $('#table_instrument_data').bootstrapTable('refresh', {'url': Flask.url_for('data.list_learner_instruments_ajax', {'tesla_id': data['tesla_id']})});
}

$(function () {
    $('#table_instrument_data').bootstrapTable();
    $('#table_instrument_data').on('post-body.bs.table', function (e, data) {
        //$('.sparkboxplot').sparkline('html', { type: 'box', minValue: 0, maxValue: 1, "height": "1.3em"});
        $('.sparkbarplot').sparkline('html', { type: 'bar', "height": "1.3em"});
    });
    $('.find_learner').on('click', function() {
        var l = Ladda.create( $(this)[0] );
        l.start();
        $('.learner-info').hide();
        $('.learner-info-loading').show();

        var mail = $(".find-learner-mail").val();
        $.ajax(Flask.url_for("api_learner.find_learner", {"mail": mail}), {
            method: 'GET'
        }).done(function(learner) {
            var tesla_id = learner['tesla_id'];
            $("#ic_information").removeClass();

            if ('correct' == learner['ic_status']) {
                $("#ic_information").addClass("fas fa-lg fa-check-circle text-success");
            } else if('outdated' == learner['ic_status']) {
                $("#ic_information").addClass("fas fa-lg fa-times-circle text-danger");
            } else if('pending' == learner['ic_status']) {
                $("#ic_information").addClass("fas fa-lg fa-exclamation-circle text-danger");
            } else if('rejected' == learner['ic_status']) {
                $("#ic_information").addClass("fas fa-lg fa-minus-circle text-danger");
            }
            $("#ic_information").text(learner['ic_message']);
            $('#current_learner_mail').text(mail);
            $('#current_learner_id').text(tesla_id);
            $.ajax(Flask.url_for("data.get_learner_data_summary", {"tesla_id": learner['tesla_id']}), {
                method: 'GET'
            }).done(function(data) {
                update_learner_data(data);
                $('.learner-info').hide();
                $('.learner-info-data').show();
            });
        }).fail(function() {
            $('.learner-info').hide();
            $('.learner-info-nodata').show();
        }).always(function() {
            l.stop()
        });
    });
});