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
 * Bootstrap Table Persian translation
 * Author: MJ Vakili <mjv.1989@Gmail.com>
 */
(function ($) {
    'use strict';

    $.fn.bootstrapTable.locales['fa-IR'] = {
        formatLoadingMessage: function () {
            return 'در حال بارگذاری, لطفا صبر کنید...';
        },
        formatRecordsPerPage: function (pageNumber) {
            return pageNumber + ' رکورد در صفحه';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return 'نمایش ' + pageFrom + ' تا ' + pageTo + ' از ' + totalRows + ' ردیف';
        },
        formatSearch: function () {
            return 'جستجو';
        },
        formatNoMatches: function () {
            return 'رکوردی یافت نشد.';
        },
        formatPaginationSwitch: function () {
            return 'نمایش/مخفی صفحه بندی';
        },
        formatRefresh: function () {
            return 'به روز رسانی';
        },
        formatToggle: function () {
            return 'تغییر نمایش';
        },
        formatColumns: function () {
            return 'سطر ها';
        },
        formatAllRows: function () {
            return 'همه';
        }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['fa-IR']);

})(jQuery);