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
 * @author zhixin wen <wenzhixin2010@gmail.com>
 * extensions: https://github.com/lukaskral/bootstrap-table-filter
 */

!function($) {

    'use strict';

    $.extend($.fn.bootstrapTable.defaults, {
        showFilter: false
    });

    var BootstrapTable = $.fn.bootstrapTable.Constructor,
        _init = BootstrapTable.prototype.init,
        _initSearch = BootstrapTable.prototype.initSearch;

    BootstrapTable.prototype.init = function () {
        _init.apply(this, Array.prototype.slice.apply(arguments));

        var that = this;
        this.$el.on('load-success.bs.table', function () {
            if (that.options.showFilter) {
                $(that.options.toolbar).bootstrapTableFilter({
                    connectTo: that.$el
                });
            }
        });
    };

    BootstrapTable.prototype.initSearch = function () {
        _initSearch.apply(this, Array.prototype.slice.apply(arguments));

        if (this.options.sidePagination !== 'server') {
            if (typeof this.searchCallback === 'function') {
                this.data = $.grep(this.options.data, this.searchCallback);
            }
        }
    };

    BootstrapTable.prototype.getData = function () {
        return (this.searchText || this.searchCallback) ? this.data : this.options.data;
    };

    BootstrapTable.prototype.getColumns = function () {
        return this.columns;
    };

    BootstrapTable.prototype.registerSearchCallback = function (callback) {
        this.searchCallback = callback;
    };

    BootstrapTable.prototype.updateSearch = function () {
        this.options.pageNumber = 1;
        this.initSearch();
        this.updatePagination();
    };

    BootstrapTable.prototype.getServerUrl = function () {
        return (this.options.sidePagination === 'server') ? this.options.url : false;
    };

    $.fn.bootstrapTable.methods.push('getColumns',
        'registerSearchCallback', 'updateSearch',
        'getServerUrl');

}(jQuery);