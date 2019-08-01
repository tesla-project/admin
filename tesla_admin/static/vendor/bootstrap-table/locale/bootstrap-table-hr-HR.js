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
 * Bootstrap Table Croatian translation
 * Author: Petra Štrbenac (petra.strbenac@gmail.com)
 * Author: Petra Štrbenac (petra.strbenac@gmail.com)
 */
(function ($) {
    'use strict';

    $.fn.bootstrapTable.locales['hr-HR'] = {
        formatLoadingMessage: function () {
            return 'Molimo pričekajte ...';
        },
        formatRecordsPerPage: function (pageNumber) {
            return pageNumber + ' broj zapisa po stranici';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return 'Prikazujem ' + pageFrom + '. - ' + pageTo + '. od ukupnog broja zapisa ' + totalRows;
        },
        formatSearch: function () {
            return 'Pretraži';
        },
        formatNoMatches: function () {
            return 'Nije pronađen niti jedan zapis';
        },
        formatPaginationSwitch: function () {
            return 'Prikaži/sakrij stranice';
        },
        formatRefresh: function () {
            return 'Osvježi';
        },
        formatToggle: function () {
            return 'Promijeni prikaz';
        },
        formatColumns: function () {
            return 'Kolone';
        },
        formatAllRows: function () {
            return 'Sve';
        }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['hr-HR']);

})(jQuery);
