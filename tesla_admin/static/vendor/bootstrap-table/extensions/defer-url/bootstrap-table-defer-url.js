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
 * When using server-side processing, the default mode of operation for
 * bootstrap-table is to simply throw away any data that currently exists in the
 * table and make a request to the server to get the first page of data to
 * display. This is fine for an empty table, but if you already have the first
 * page of data displayed in the plain HTML, it is a waste of resources. As
 * such, you can use data-defer-url instead of data-url to allow you to instruct
 * bootstrap-table to not make that initial request, rather it will use the data
 * already on the page.
 *
 * @author: Ruben Suarez
 * @webSite: http://rubensa.eu.org
 * @version: v1.0.0
 */

(function($) {
    'use strict';

    $.extend($.fn.bootstrapTable.defaults, {
        deferUrl : undefined
    });

    var BootstrapTable = $.fn.bootstrapTable.Constructor, _init = BootstrapTable.prototype.init;

    BootstrapTable.prototype.init = function() {
        _init.apply(this, Array.prototype.slice.apply(arguments));

        if (this.options.deferUrl) {
            this.options.url = this.options.deferUrl;
        }
    }
})(jQuery);