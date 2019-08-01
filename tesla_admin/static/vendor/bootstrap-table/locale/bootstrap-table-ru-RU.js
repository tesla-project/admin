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
 * Bootstrap Table Russian translation
 * Author: Dunaevsky Maxim <dunmaksim@yandex.ru>
 */
(function ($) {
    'use strict';
    $.fn.bootstrapTable.locales['ru-RU'] = {
        formatLoadingMessage: function () {
            return 'Пожалуйста, подождите, идёт загрузка...';
        },
        formatRecordsPerPage: function (pageNumber) {
            return pageNumber + ' записей на страницу';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return 'Записи с ' + pageFrom + ' по ' + pageTo + ' из ' + totalRows;
        },
        formatSearch: function () {
            return 'Поиск';
        },
        formatNoMatches: function () {
            return 'Ничего не найдено';
        },
        formatRefresh: function () {
            return 'Обновить';
        },
        formatToggle: function () {
            return 'Переключить';
        },
        formatColumns: function () {
            return 'Колонки';
        },
        formatClearFilters: function () {
            return 'Очистить фильтры';
        },
        formatMultipleSort: function () {
            return 'Множественная сортировка';
        },
        formatAddLevel: function () {
            return 'Добавить уровень';
        },
        formatDeleteLevel: function () {
            return 'Удалить уровень';
        },
        formatColumn: function () {
            return 'Колонка';
        },
        formatOrder: function () {
            return 'Порядок';
        },
        formatSortBy: function () {
            return 'Сортировать по';
        },
        formatThenBy: function () {
            return 'затем по';
        },
        formatSort: function () {
            return 'Сортировать';
        },
        formatCancel: function () {
            return 'Отмена';
        },
        formatDuplicateAlertTitle: function () {
            return 'Дублирование колонок!';
        },
        formatDuplicateAlertDescription: function () {
            return 'Удалите, пожалуйста, дублирующую колонку, или замените ее на другую.';
        }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['ru-RU']);

})(jQuery);
