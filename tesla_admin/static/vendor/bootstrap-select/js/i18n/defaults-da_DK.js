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
    noneSelectedText: 'Intet valgt',
    noneResultsText: 'Ingen resultater fundet {0}',
    countSelectedText: function (numSelected, numTotal) {
      return (numSelected == 1) ? "{0} valgt" : "{0} valgt";
    },
    maxOptionsText: function (numAll, numGroup) {
      return [
        (numAll == 1) ? 'Begrænsning nået (max {n} valgt)' : 'Begrænsning nået (max {n} valgte)',
        (numGroup == 1) ? 'Gruppe-begrænsning nået (max {n} valgt)' : 'Gruppe-begrænsning nået (max {n} valgte)'
      ];
    },
    selectAllText: 'Markér alle',
    deselectAllText: 'Afmarkér alle',
    multipleSeparator: ', '
  };
})(jQuery);


}));
