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
 * Bootstrap Table English translation
 * Author: Zhixin Wen<wenzhixin2010@gmail.com>
 */
(function ($) {
    'use strict';

    $.fn.bootstrapTable.locales['ar-SA'] = {
        formatLoadingMessage: function () {
            return 'جاري التحميل, يرجى الإنتظار...';
        },
        formatRecordsPerPage: function (pageNumber) {
            return pageNumber + ' سجل لكل صفحة';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return 'الظاهر ' + pageFrom + ' إلى ' + pageTo + ' من ' + totalRows + ' سجل';
        },
        formatSearch: function () {
            return 'بحث';
        },
        formatNoMatches: function () {
            return 'لا توجد نتائج مطابقة للبحث';
        },
        formatPaginationSwitch: function () {
            return 'إخفاء\إظهار ترقيم الصفحات';
        },
        formatRefresh: function () {
            return 'تحديث';
        },
        formatToggle: function () {
            return 'تغيير';
        },
        formatColumns: function () {
            return 'أعمدة';
        }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['ar-SA']);

})(jQuery);
