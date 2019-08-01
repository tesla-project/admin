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
    noneSelectedText: 'មិនមានអ្វីបានជ្រើសរើស',
    noneResultsText: 'មិនមានលទ្ធផល {0}',
    countSelectedText: function (numSelected, numTotal) {
      return (numSelected == 1) ? "{0} ធាតុដែលបានជ្រើស" : "{0} ធាតុដែលបានជ្រើស";
    },
    maxOptionsText: function (numAll, numGroup) {
      return [
        (numAll == 1) ? 'ឈានដល់ដែនកំណត់ ( {n} ធាតុអតិបរមា)' : 'អតិបរមាឈានដល់ដែនកំណត់ ( {n} ធាតុ)',
        (numGroup == 1) ? 'ដែនកំណត់ក្រុមឈានដល់ ( {n} អតិបរមាធាតុ)' : 'អតិបរមាក្រុមឈានដល់ដែនកំណត់ ( {n} ធាតុ)'
      ];
    },
    selectAllText: 'ជ្រើស​យក​ទាំងអស់',
    deselectAllText: 'មិនជ្រើស​យក​ទាំងអស',
    multipleSeparator: ', '
  };
})(jQuery);


}));
