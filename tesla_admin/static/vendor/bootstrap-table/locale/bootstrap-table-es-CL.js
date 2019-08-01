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
 * Traducción de librería Bootstrap Table a Español (Chile)
 * @author Brian Álvarez Azócar
 * email brianalvarezazocar@gmail.com
 */
(function($) {
  'use strict';

  $.fn.bootstrapTable.locales['es-CL'] = {
    formatLoadingMessage: function() {
      return 'Cargando, espere por favor...';
    },
    formatRecordsPerPage: function(pageNumber) {
      return pageNumber + ' filas por p\u00E1gina';
    },
    formatShowingRows: function(pageFrom, pageTo, totalRows) {
      return 'Mostrando ' + pageFrom + ' a ' + pageTo + ' de ' + totalRows + ' filas';
    },
    formatSearch: function() {
      return 'Buscar';
    },
    formatNoMatches: function() {
      return 'No se encontraron registros';
    },
    formatPaginationSwitch: function() {
      return 'Ocultar/Mostrar paginaci\u00F3n';
    },
    formatRefresh: function() {
      return 'Refrescar';
    },
    formatToggle: function() {
      return 'Cambiar';
    },
    formatColumns: function() {
      return 'Columnas';
    },
    formatAllRows: function() {
      return 'Todo';
    }
  };

  $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['es-CL']);

})(jQuery);
