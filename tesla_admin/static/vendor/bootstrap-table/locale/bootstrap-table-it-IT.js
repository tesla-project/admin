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
 * Bootstrap Table Italian translation
 * Author: Davide Renzi<davide.renzi@gmail.com>
 * Author: Davide Borsatto <davide.borsatto@gmail.com>
 * Author: Alessio Felicioni <alessio.felicioni@gmail.com>
 */
(function ($) {
    'use strict';

    $.fn.bootstrapTable.locales['it-IT'] = {
        formatLoadingMessage: function () {
            return 'Caricamento in corso...';
        },
        formatRecordsPerPage: function (pageNumber) {
            return pageNumber + ' elementi per pagina';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return 'Elementi mostrati da ' + pageFrom + ' a ' + pageTo + ' (Numero totali di elementi ' + totalRows + ')';
        },
        formatSearch: function () {
            return 'Cerca';
        },
        formatNoMatches: function () {
            return 'Nessun elemento trovato';
        },
        formatPaginationSwitch: function () {
            return 'Nascondi/Mostra paginazione';
        },
        formatRefresh: function () {
            return 'Aggiorna';
        },
        formatToggle: function () {
            return 'Attiva/Disattiva';
        },
        formatColumns: function () {
            return 'Colonne';
        },
        formatAllRows: function () {
            return 'Tutto';
        },
        formatExport: function () {
            return 'Esporta dati';
        },
        formatClearFilters: function () {
            return 'Pulisci filtri';
        }
        
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['it-IT']);

})(jQuery);
