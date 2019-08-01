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
 * Bootstrap Table Dutch translation
 * Author: Your Name <info@a2hankes.nl>
 */
(function($) {
    'use strict';

    $.fn.bootstrapTable.locales['nl-NL'] = {
        formatLoadingMessage: function() {
            return 'Laden, even geduld...';
        },
        formatRecordsPerPage: function(pageNumber) {
            return pageNumber + ' records per pagina';
        },
        formatShowingRows: function(pageFrom, pageTo, totalRows) {
            return 'Toon ' + pageFrom + ' tot ' + pageTo + ' van ' + totalRows + ' record' + ((totalRows > 1) ? 's' : '');
        },
        formatDetailPagination: function(totalRows) {
            return 'Toon ' + totalRows + ' record' + ((totalRows > 1) ? 's' : '');
        },
        formatSearch: function() {
            return 'Zoeken';
        },
        formatNoMatches: function() {
            return 'Geen resultaten gevonden';
        },
        formatRefresh: function() {
            return 'Vernieuwen';
        },
        formatToggle: function() {
            return 'Omschakelen';
        },
        formatColumns: function() {
            return 'Kolommen';
        },
        formatAllRows: function() {
            return 'Alle';
        },
        formatPaginationSwitch: function() {
            return 'Verberg/Toon paginatie';
        },
        formatExport: function() {
            return 'Exporteer data';
        },
        formatClearFilters: function() {
            return 'Verwijder filters';
        }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['nl-NL']);

})(jQuery);
