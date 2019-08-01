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
 * Bootstrap Table Indonesian translation
 * Author: Andre Gardiner<andre@sirdre.com> 
 */
(function ($) {
    'use strict';

    $.fn.bootstrapTable.locales['id-ID'] = {
        formatLoadingMessage: function () {
            return 'Memuat, mohon tunggu...';
        },
        formatRecordsPerPage: function (pageNumber) {
            return pageNumber + ' baris per halaman';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return 'Menampilkan ' + pageFrom + ' sampai ' + pageTo + ' dari ' + totalRows + ' baris';
        }, 
        formatSearch: function () {
            return 'Pencarian';
        },
        formatNoMatches: function () {
            return 'Tidak ditemukan data yang cocok';
        },
        formatPaginationSwitch: function () {
            return 'Sembunyikan/Tampilkan halaman';
        },
        formatRefresh: function () {
            return 'Muat ulang';
        },
        formatToggle: function () {
            return 'Beralih';
        },
        formatColumns: function () {
            return 'kolom';
        },
        formatAllRows: function () {
            return 'Semua';
        },
        formatExport: function () {
            return 'Ekspor data';
        },
        formatClearFilters: function () {
            return 'Bersihkan filter';
        }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['id-ID']);

})(jQuery);
