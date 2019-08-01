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

/**
 * Bootstrap Table Basque (Basque Country) translation
 * Author: Iker Ibarguren Berasaluze<ikerib@gmail.com>
 */
(function ($) {
    'use strict';

    $.fn.bootstrapTable.locales['eu-EU'] = {
        formatLoadingMessage: function () {
            return 'Itxaron mesedez...';
        },
        formatRecordsPerPage: function (pageNumber) {
            return pageNumber + ' emaitza orriko.';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return totalRows + ' erregistroetatik ' + pageFrom + 'etik ' + pageTo +'erakoak erakusten.';
        },
        formatSearch: function () {
            return 'Bilatu';
        },
        formatNoMatches: function () {
            return 'Ez da emaitzarik aurkitu';
        },
        formatPaginationSwitch: function () {
            return 'Ezkutatu/Erakutsi orrikatzea';
        },
        formatRefresh: function () {
            return 'Eguneratu';
        },
        formatToggle: function () {
            return 'Ezkutatu/Erakutsi';
        },
        formatColumns: function () {
            return 'Zutabeak';
        },
        formatAllRows: function () {
            return 'Guztiak';
        }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['eu-EU']);

})(jQuery);
