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
 * Bootstrap Table Portuguese Portugal Translation
 * Author: Burnspirit<burnspirit@gmail.com>
 */
(function ($) {
    'use strict';

    $.fn.bootstrapTable.locales['pt-PT'] = {
        formatLoadingMessage: function () {
            return 'A carregar, por favor aguarde...';
        },
        formatRecordsPerPage: function (pageNumber) {
            return pageNumber + ' registos por p&aacute;gina';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return 'A mostrar ' + pageFrom + ' at&eacute; ' + pageTo + ' de ' + totalRows + ' linhas';
        },
        formatSearch: function () {
            return 'Pesquisa';
        },
        formatNoMatches: function () {
            return 'Nenhum registo encontrado';
        },
        formatPaginationSwitch: function () {
            return 'Esconder/Mostrar pagina&ccedil&atilde;o';
        },
        formatRefresh: function () {
            return 'Atualizar';
        },
        formatToggle: function () {
            return 'Alternar';
        },
        formatColumns: function () {
            return 'Colunas';
        },
        formatAllRows: function () {
            return 'Tudo';
        }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['pt-PT']);

})(jQuery);
