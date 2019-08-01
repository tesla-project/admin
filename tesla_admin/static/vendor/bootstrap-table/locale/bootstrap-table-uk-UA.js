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
 * Bootstrap Table Ukrainian translation
 * Author: Vitaliy Timchenko <vitaliy.timchenko@gmail.com>
 */
 (function ($) {
    'use strict';
    
    $.fn.bootstrapTable.locales['uk-UA'] = {
        formatLoadingMessage: function () {
            return 'Завантаження, будь ласка, зачекайте...';
        },
        formatRecordsPerPage: function (pageNumber) {
            return pageNumber + ' записів на сторінку';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return 'Показано з ' + pageFrom + ' по ' + pageTo + '. Всього: ' + totalRows;
        },
        formatSearch: function () {
            return 'Пошук';
        },
        formatNoMatches: function () {
            return 'Не знайдено жодного запису';
        },
        formatRefresh: function () {
            return 'Оновити';
        },
        formatToggle: function () {
            return 'Змінити';
        },
        formatColumns: function () {
            return 'Стовпці';
        },
        formatClearFilters: function () {
            return 'Очистити фільтри';
        },
        formatMultipleSort: function () {
            return 'Сортування за кількома стовпцями';
        },
        formatAddLevel: function () {
            return 'Додати рівень';
        },
        formatDeleteLevel: function () {
            return 'Видалити рівень';
        },
        formatColumn: function () {
            return 'Стовпець';
        },
        formatOrder: function () {
            return 'Порядок';
        },
        formatSortBy: function () {
            return 'Сортувати за';
        },
        formatThenBy: function () {
            return 'потім за';
        },
        formatSort: function () {
            return 'Сортувати';
        },
        formatCancel: function () {
            return 'Скасувати';
        },
        formatDuplicateAlertTitle: function () {
            return 'Дублювання стовпців!';
        },
        formatDuplicateAlertDescription: function () {
            return 'Видаліть, будь ласка, дублюючий стовпець, або замініть його на інший.';
        }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['uk-UA']);

})(jQuery);
