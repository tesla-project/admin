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
 * Bootstrap Table Urdu translation
 * Author: Malik <me@malikrizwan.com>
 */
(function ($) {
    'use strict';

    $.fn.bootstrapTable.locales['ur-PK'] = {
        formatLoadingMessage: function () {
            return 'براۓ مہربانی انتظار کیجئے';
        },
        formatRecordsPerPage: function (pageNumber) {
            return pageNumber + ' ریکارڈز فی صفہ ';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return 'دیکھیں ' + pageFrom + ' سے ' + pageTo + ' کے ' +  totalRows + 'ریکارڈز';
        },
        formatSearch: function () {
            return 'تلاش';
        },
        formatNoMatches: function () {
            return 'کوئی ریکارڈ نہیں ملا';
        },
        formatRefresh: function () {
            return 'تازہ کریں';
        },
        formatToggle: function () {
            return 'تبدیل کریں';
        },
        formatColumns: function () {
            return 'کالم';
        }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['ur-PK']);

})(jQuery);
