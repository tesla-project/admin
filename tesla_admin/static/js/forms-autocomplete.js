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
    $.get('data/countries.json', function (data) {
        $("#typeahead2").typeahead({ source: data.countries });
    }, 'json');


    $('#typeahead3').typeahead({
        displayText: function (item) {
            return item.name + ' ' + item.surname + ', ' + item.company
        },
        afterSelect: function (item) {
            this.$element[0].value = item.email
        },
        source: [
            { "name": "Alyce", "surname": "White", "company": "Combot", "email": "alycewhite@combot.com", "city": "Talpa" },
            { "name": "Santos", "surname": "Pierce", "company": "Franscene", "email": "santospierce@franscene.com", "city": "Vienna" },
            { "name": "Deirdre", "surname": "Reed", "company": "Whiskey Comp.", "email": "deirdrereed@whiskeycomp.com", "city": "Belva" },
            { "name": "Whitaker", "surname": "Brennan", "company": "Opticom", "email": "whitakerbrennan@opticom.com", "city": "Lodoga" },
            { "name": "Kristin", "surname": "Norman", "company": "Irack", "email": "kristinnorman@irack.com", "city": "Bodega" }
        ]
    });

    $('#typeahead4').typeahead({
        source: ["item 1","item 2","item 3"]
    });

});

