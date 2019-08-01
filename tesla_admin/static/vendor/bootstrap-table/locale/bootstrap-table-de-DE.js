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
* Bootstrap Table German translation
* Author: Paul Mohr - Sopamo<p.mohr@sopamo.de>
*/
(function ($) {
  'use strict';

  $.fn.bootstrapTable.locales['de-DE'] = {
    formatLoadingMessage: function () {
      return 'Lade, bitte warten...';
    },
    formatRecordsPerPage: function (pageNumber) {
      return pageNumber + ' Zeilen pro Seite.';
    },
    formatShowingRows: function (pageFrom, pageTo, totalRows) {
      return 'Zeige Zeile ' + pageFrom + ' bis ' + pageTo + ' von ' + totalRows + ' Zeilen' + ((totalRows > 1) ? "n" : "")+".";
    },
    formatDetailPagination: function (totalRows) {
      return 'Zeige ' + totalRows + ' Zeile' + ((totalRows > 1) ? "n" : "")+".";
    },
    formatSearch: function () {
      return 'Suchen';
    },
    formatNoMatches: function () {
      return 'Keine passenden Ergebnisse gefunden';
    },
    formatPaginationSwitch: function () {
      return 'Verstecke/Zeige Nummerierung';
    },
    formatRefresh: function () {
      return 'Neu laden';
    },
    formatToggle: function () {
      return 'Umschalten';
    },
    formatColumns: function () {
      return 'Spalten';
    },
    formatAllRows: function () {
      return 'Alle';
    },
    formatExport: function () {
      return 'Datenexport';
    },
    formatClearFilters: function () {
      return 'Lösche Filter';
     }
  };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['de-DE']);

})(jQuery);
