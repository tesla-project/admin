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
 * Bootstrap Table Estonian translation
 * Author: kristjan@logist.it>
 */
(function ($) {
    'use strict';

    $.fn.bootstrapTable.locales['et-EE'] = {
        formatLoadingMessage: function () {
            return 'Päring käib, palun oota...';
        },
        formatRecordsPerPage: function (pageNumber) {
            return pageNumber + ' rida lehe kohta';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return 'Näitan tulemusi ' + pageFrom + ' kuni ' + pageTo + ' - kokku ' + totalRows + ' tulemust';
        },
        formatSearch: function () {
            return 'Otsi';
        },
        formatNoMatches: function () {
            return 'Päringu tingimustele ei vastanud ühtegi tulemust';
        },
        formatPaginationSwitch: function () {
            return 'Näita/Peida lehtedeks jagamine';
        },
        formatRefresh: function () {
            return 'Värskenda';
        },
        formatToggle: function () {
            return 'Lülita';
        },
        formatColumns: function () {
            return 'Veerud';
        },
        formatAllRows: function () {
            return 'Kõik';
        }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['et-EE']);

})(jQuery);