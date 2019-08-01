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
 * Bootstrap Table Uzbek translation
 * Author: Nabijon Masharipov <mnabijonz@gmail.com>
 */
(function ($) {
    'use strict';

    $.fn.bootstrapTable.locales['uz-Latn-UZ'] = {
        formatLoadingMessage: function () {
            return 'Yuklanyapti, iltimos kuting...';
        },
        formatRecordsPerPage: function (pageNumber) {
            return pageNumber + ' qator har sahifada';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return 'Ko\'rsatypati ' + pageFrom + ' dan ' + pageTo + ' gacha ' + totalRows + ' qatorlarni';
        },
        formatSearch: function () {
            return 'Qidirish';
        },
        formatNoMatches: function () {
            return 'Hech narsa topilmadi';
        },
        formatPaginationSwitch: function () {
            return 'Sahifalashni yashirish/ko\'rsatish';
        },
        formatRefresh: function () {
            return 'Yangilash';
        },
        formatToggle: function () {
            return 'Ko\'rinish';
        },
        formatColumns: function () {
            return 'Ustunlar';
        },
        formatAllRows: function () {
            return 'Hammasi';
        },
        formatExport: function () {
            return 'Eksport';
        },
        formatClearFilters: function () {
            return 'Filtrlarni tozalash';
        }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['uz-Latn-UZ']);

})(jQuery);
