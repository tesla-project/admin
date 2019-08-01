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

$(function () {
    var basic = document.getElementById('basicNoUISlider');

    noUiSlider.create(basic, {
        start: [20, 80],
        range: {
            'min': [0],
            'max': [100]
        }
    });

    var step = document.getElementById('stepNoUISlider');

    noUiSlider.create(step, {
        start: [200, 1000],
        range: {
            'min': [0],
            'max': [1800]
        },
        step: 100,
        tooltips: true,
        connect: true
    });

    $('.input-datepicker').datepicker({
        format: 'mm/dd/yyyy'
    });

    $('.input-datepicker-autoclose').datepicker({
        autoclose: true,
        format: 'mm/dd/yyyy'
    });

    $('.input-datepicker-multiple').datepicker({
        multidate: true,
        format: 'mm/dd/yyyy'
    });

    $('.input-datepicker-range').datepicker({
        format: 'mm/dd/yyyy'
    });

    $("input[name='touchspin0']").TouchSpin({
        buttondown_class: 'btn btn-secondary',
        buttonup_class: 'btn btn-secondary'
    });
    $("input[name='touchspin1']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.1,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%',
        postfix_extraclass: "input-group-text",
        buttondown_class: 'btn btn-secondary',
        buttonup_class: 'btn btn-secondary'
    });

    $("input[name='touchspin2']").TouchSpin({
        min: -1000000000,
        max: 1000000000,
        step: 50,
        maxboostedstep: 10000000,
        prefix: '$',
        prefix_extraclass: "input-group-text",
        buttondown_class: 'btn btn-secondary',
        buttonup_class: 'btn btn-secondary'
    });

    $('.selectpicker-primary').selectpicker({
        style: 'btn-primary',
        size: 4
    });

    $('.selectpicker-secondary').selectpicker({
        style: 'btn-secondary',
        size: 4
    });

    $('.selectpicker-light').selectpicker({
        style: 'btn-outline-light',
        size: 4
    });

    $('#multiselect1').multiSelect();

});

