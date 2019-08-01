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
 * Bootstrap Table Turkish translation
 * Author: Emin Şen
 * Author: Sercan Cakir <srcnckr@gmail.com>
 */
(function ($) {
    'use strict';

    $.fn.bootstrapTable.locales['tr-TR'] = {
        formatLoadingMessage: function () {
            return 'Yükleniyor, lütfen bekleyin...';
        },
        formatRecordsPerPage: function (pageNumber) {
            return 'Sayfa başına ' + pageNumber + ' kayıt.';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return totalRows + ' kayıttan ' + pageFrom + '-' + pageTo + ' arası gösteriliyor.';
        },
        formatSearch: function () {
            return 'Ara';
        },
        formatNoMatches: function () {
            return 'Eşleşen kayıt bulunamadı.';
        },
        formatRefresh: function () {
            return 'Yenile';
        },
        formatToggle: function () {
            return 'Değiştir';
        },
        formatColumns: function () {
            return 'Sütunlar';
        },
        formatAllRows: function () {
            return 'Tüm Satırlar';
        }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['tr-TR']);

})(jQuery);
