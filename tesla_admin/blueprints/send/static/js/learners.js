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

function update_efective_options(options, instruments) {
    $.each($('input[name="options"]'), function() {
        if (options.indexOf($(this).val()) >= 0) {
            $(this).prop('checked', true);
        } else {
            $(this).prop('checked', false);
        }
    });
    $.each($('input[name="instruments"]'), function() {
        if (instruments.indexOf(parseInt($(this).val())) >= 0) {
            $(this).prop('checked', true);
        } else {
            $(this).prop('checked', false);
        }
    });
}

$(function () {
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
            $.ajax(Flask.url_for("send.get_learner_categories", {"tesla_id": learner['tesla_id']}), {
                method: 'GET'
            }).done(function(data) {
                var options = data['options'];
                var instruments = data['instruments'];
                update_efective_options(options, instruments);
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

    $("#learner_cats").on('change', function(){
        var tesla_id = $('#current_learner_id').text();

        $.ajax(Flask.url_for("send.set_learner_categories", {"tesla_id": tesla_id}), {
            method: 'POST',
            data: JSON.stringify({ categories: $(this).val() }),
            contentType: "application/json; charset=utf-8",
            dataType: "json"
        }).done(function(data) {
            var options = data['options'];
            var instruments = data['instruments'];
            update_efective_options(options, instruments);
        });
    })
});