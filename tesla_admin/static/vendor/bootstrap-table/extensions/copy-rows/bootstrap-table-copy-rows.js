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
 * @author Homer Glascock <HopGlascock@gmail.com>
 * @version: v1.0.0
 */

 !function ($) {
    "use strict";

    var calculateObjectValue = $.fn.bootstrapTable.utils.calculateObjectValue,
        sprintf = $.fn.bootstrapTable.utils.sprintf;

    var copytext = function (text) {
        var textField = document.createElement('textarea');
        $(textField).html(text);
        document.body.appendChild(textField);
        textField.select();

        try {
            document.execCommand('copy');
        }
        catch (e) {
            console.log("Oops, unable to copy");
        }
        $(textField).remove();
    };

    $.extend($.fn.bootstrapTable.defaults, {
        copyBtn: false,
        copyWHiddenBtn: false,
        copyDelemeter: ", "
    });

    $.fn.bootstrapTable.methods.push('copyColumnsToClipboard', 'copyColumnsToClipboardWithHidden');

    var BootstrapTable = $.fn.bootstrapTable.Constructor,
        _initToolbar = BootstrapTable.prototype.initToolbar;

    BootstrapTable.prototype.initToolbar = function () {

        _initToolbar.apply(this, Array.prototype.slice.apply(arguments));

        var that = this,
            $btnGroup = this.$toolbar.find('>.btn-group');

        if (this.options.clickToSelect || this.options.singleSelect) {

            if (this.options.copyBtn) {
                var copybtn = "<button class='btn btn-default' id='copyBtn'><span class='glyphicon glyphicon-copy icon-pencil'></span></button>";
                $btnGroup.append(copybtn);
                $btnGroup.find('#copyBtn').click(function () { that.copyColumnsToClipboard(); });
            }

            if (this.options.copyWHiddenBtn) {
                var copyhiddenbtn = "<button class='btn btn-default' id='copyWHiddenBtn'><span class='badge'><span class='glyphicon glyphicon-copy icon-pencil'></span></span></button>";
                $btnGroup.append(copyhiddenbtn);
                $btnGroup.find('#copyWHiddenBtn').click(function () { that.copyColumnsToClipboardWithHidden(); });
            }
        }
    };

    BootstrapTable.prototype.copyColumnsToClipboard = function () {
        var that = this,
            ret = "",
            delimet = this.options.copyDelemeter;

        $.each(that.getSelections(), function (index, row) {
            $.each(that.options.columns[0], function (indy, column) {
                if (column.field !== "state" && column.field !== "RowNumber" && column.visible) {
                    if (row[column.field] !== null) {
                        ret += calculateObjectValue(column, that.header.formatters[indy], [row[column.field], row, index], row[column.field]);
                    }
                    ret += delimet;
                }
            });

            ret += "\r\n";
        });

        copytext(ret);
    };

    BootstrapTable.prototype.copyColumnsToClipboardWithHidden = function () {
        var that = this,
            ret = "",
            delimet = this.options.copyDelemeter;

        $.each(that.getSelections(), function (index, row) {
            $.each(that.options.columns[0], function (indy, column) {
                if (column.field != "state" && column.field !== "RowNumber") {
                    if (row[column.field] !== null) {
                        ret += calculateObjectValue(column, that.header.formatters[indy], [row[column.field], row, index], row[column.field]);
                    }
                    ret += delimet;
                }
            });

            ret += "\r\n";
        });

        copytext(ret);
    };
}(jQuery);