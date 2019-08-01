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
 * Bootstrap Table Hebrew translation
 * Author: legshooter
 */
(function ($) {
    'use strict';

    $.fn.bootstrapTable.locales['he-IL'] = {
        formatLoadingMessage: function () {
            return 'טוען, נא להמתין...';
        },
        formatRecordsPerPage: function (pageNumber) {
            return pageNumber + ' שורות בעמוד';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return 'מציג ' + pageFrom + ' עד ' + pageTo + ' מ-' + totalRows + ' שורות';
        },
        formatSearch: function () {
            return 'חיפוש';
        },
        formatNoMatches: function () {
            return 'לא נמצאו רשומות תואמות';
        },
        formatPaginationSwitch: function () {
            return 'הסתר/הצג מספור דפים';
        },
        formatRefresh: function () {
            return 'רענן';
        },
        formatToggle: function () {
            return 'החלף תצוגה';
        },
        formatColumns: function () {
            return 'עמודות';
        },
        formatAllRows: function () {
            return 'הכל';
        }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['he-IL']);

})(jQuery);
