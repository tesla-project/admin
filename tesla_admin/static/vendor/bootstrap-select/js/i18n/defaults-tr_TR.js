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

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module unless amdModuleId is set
    define(["jquery"], function (a0) {
      return (factory(a0));
    });
  } else if (typeof module === 'object' && module.exports) {
    // Node. Does not work with strict CommonJS, but
    // only CommonJS-like environments that support module.exports,
    // like Node.
    module.exports = factory(require("jquery"));
  } else {
    factory(root["jQuery"]);
  }
}(this, function (jQuery) {

(function ($) {
  $.fn.selectpicker.defaults = {
    noneSelectedText: 'Hiçbiri seçilmedi',
    noneResultsText: 'Hiçbir sonuç bulunamadı {0}',
    countSelectedText: function (numSelected, numTotal) {
      return (numSelected == 1) ? "{0} öğe seçildi" : "{0} öğe seçildi";
    },
    maxOptionsText: function (numAll, numGroup) {
      return [
        (numAll == 1) ? 'Limit aşıldı (maksimum {n} sayıda öğe )' : 'Limit aşıldı (maksimum {n} sayıda öğe)',
        (numGroup == 1) ? 'Grup limiti aşıldı (maksimum {n} sayıda öğe)' : 'Grup limiti aşıldı (maksimum {n} sayıda öğe)'
      ];
    },
    selectAllText: 'Tümünü Seç',
    deselectAllText: 'Seçiniz',
    multipleSeparator: ', '
  };
})(jQuery);


}));
