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
 * Bootstrap Table Spanish (México) translation (Obtenido de traducción de Argentina)
 * Author: Felix Vera (felix.vera@gmail.com) 
 * Copiado: Mauricio Vera (mauricioa.vera@gmail.com)
 * Revisión: J Manuel Corona (jmcg92@gmail.com) (13/Feb/2018).
 */
(function ($) {
    'use strict';

    $.fn.bootstrapTable.locales['es-MX'] = {
        formatLoadingMessage: function () {
            return 'Cargando, espere por favor...';
        },
        formatRecordsPerPage: function (pageNumber) {
            return pageNumber + ' registros por página';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return 'Mostrando ' + pageFrom + ' a ' + pageTo + ' de ' + totalRows + ' filas';
        },
        formatDetailPagination: function (totalRows) {
            return 'Mostrando ' + totalRows + ' filas';
        },
        formatSearch: function () {
            return 'Buscar';
        },
        formatNoMatches: function () {
            return 'No se encontraron registros que coincidan';
        },
        formatPaginationSwitch: function () {
            return 'Mostrar/ocultar paginación';
        },
        formatRefresh: function () {
            return 'Actualizar';
        },
        formatToggle: function () {
            return 'Cambiar vista';
        },
        formatFullscreen: function () {
            return 'Pantalla completa';
        },
        formatColumns: function () {
            return 'Columnas';
        },
        formatAllRows: function () {
            return 'Todo';
        }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['es-MX']);

})(jQuery);
