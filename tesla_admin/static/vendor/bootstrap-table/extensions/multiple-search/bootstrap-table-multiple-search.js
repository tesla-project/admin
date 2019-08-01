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
 * @author: Dennis Hernández
 * @webSite: http://djhvscf.github.io/Blog
 * @version: v1.0.0
 */

!function ($) {

    'use strict';

    $.extend($.fn.bootstrapTable.defaults, {
        multipleSearch: false,
	    delimeter: " "
    });

    var BootstrapTable = $.fn.bootstrapTable.Constructor,
        _initSearch = BootstrapTable.prototype.initSearch;

    BootstrapTable.prototype.initSearch = function () {
        if (this.options.multipleSearch) {
            if (this.searchText === undefined) {
                return;
            }
            var strArray = this.searchText.split(this.options.delimeter),
                that = this,
                f = $.isEmptyObject(this.filterColumns) ? null : this.filterColumns,
                dataFiltered = [];

            if (strArray.length === 1) {
                _initSearch.apply(this, Array.prototype.slice.apply(arguments));
            } else {
                for (var i = 0; i < strArray.length; i++) {
                    var str = strArray[i].trim();
                    dataFiltered = str ? $.grep(dataFiltered.length === 0 ? this.options.data : dataFiltered, function (item, i) {
                        for (var key in item) {
                            key = $.isNumeric(key) ? parseInt(key, 10) : key;
                            var value = item[key],
                                column = that.columns[that.fieldsColumnsIndex[key]],
                                j = $.inArray(key, that.header.fields);

                            // Fix #142: search use formated data
                            if (column && column.searchFormatter) {
                                value = $.fn.bootstrapTable.utils.calculateObjectValue(column,
                                    that.header.formatters[j], [value, item, i], value);
                            }

                            var index = $.inArray(key, that.header.fields);
                            if (index !== -1 && that.header.searchables[index] && (typeof value === 'string' || typeof value === 'number')) {
                                if (that.options.strictSearch) {
                                    if ((value + '').toLowerCase() === str) {
                                        return true;
                                    }
                                } else {
                                    if ((value + '').toLowerCase().indexOf(str) !== -1) {
                                        return true;
                                    }
                                }
                            }
                        }
                        return false;
                    }) : this.data;
                }

                this.data = dataFiltered;
            }
        } else {
            _initSearch.apply(this, Array.prototype.slice.apply(arguments));
        }
    };

}(jQuery);
