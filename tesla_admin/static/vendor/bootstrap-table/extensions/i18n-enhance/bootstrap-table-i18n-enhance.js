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
 * @author: Jewway
 * @version: v1.0.0
 */

!function ($) {
  'use strict';

  var BootstrapTable = $.fn.bootstrapTable.Constructor;

  BootstrapTable.prototype.changeTitle = function (locale) {
    $.each(this.options.columns, function (idx, columnList) {
      $.each(columnList, function (idx, column) {
        if (column.field) {
          column.title = locale[column.field];
        }
      });
    });
    this.initHeader();
    this.initBody();
    this.initToolbar();
  };

  BootstrapTable.prototype.changeLocale = function (localeId) {
    this.options.locale = localeId;
    this.initLocale();
    this.initPagination();
    this.initBody();
    this.initToolbar();
  };

  $.fn.bootstrapTable.methods.push('changeTitle');
  $.fn.bootstrapTable.methods.push('changeLocale');

}(jQuery);
