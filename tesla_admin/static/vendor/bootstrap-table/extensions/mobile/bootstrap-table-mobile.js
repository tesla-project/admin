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
 * @version: v1.1.0
 */

!function ($) {

    'use strict';

    var showHideColumns = function (that, checked) {
        if (that.options.columnsHidden.length > 0 ) {
            $.each(that.columns, function (i, column) {
                if (that.options.columnsHidden.indexOf(column.field) !== -1) {
                    if (column.visible !== checked) {
                        that.toggleColumn(that.fieldsColumnsIndex[column.field], checked, true);
                    }
                }
            });
        }
    };

    var resetView = function (that) {
        if (that.options.height || that.options.showFooter) {
            setTimeout(function(){
                that.resetView.call(that);
            }, 1);
        }
    };

    var changeView = function (that, width, height) {
        if (that.options.minHeight) {
            if ((width <= that.options.minWidth) && (height <= that.options.minHeight)) {
                conditionCardView(that);
            } else if ((width > that.options.minWidth) && (height > that.options.minHeight)) {
                conditionFullView(that);
            }
        } else {
            if (width <= that.options.minWidth) {
                conditionCardView(that);
            } else if (width > that.options.minWidth) {
                conditionFullView(that);
            }
        }

        resetView(that);
    };

    var conditionCardView = function (that) {
        changeTableView(that, false);
        showHideColumns(that, false);
    };

    var conditionFullView = function (that) {
        changeTableView(that, true);
        showHideColumns(that, true);
    };

    var changeTableView = function (that, cardViewState) {
        that.options.cardView = cardViewState;
        that.toggleView();
    };

    var debounce = function(func,wait) {
        var timeout;
        return function() {
            var context = this,
                args = arguments;
            var later = function() {
                timeout = null;
                func.apply(context,args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    };

    $.extend($.fn.bootstrapTable.defaults, {
        mobileResponsive: false,
        minWidth: 562,
        minHeight: undefined,
        heightThreshold: 100, // just slightly larger than mobile chrome's auto-hiding toolbar
        checkOnInit: true,
        columnsHidden: []
    });

    var BootstrapTable = $.fn.bootstrapTable.Constructor,
        _init = BootstrapTable.prototype.init;

    BootstrapTable.prototype.init = function () {
        _init.apply(this, Array.prototype.slice.apply(arguments));

        if (!this.options.mobileResponsive) {
            return;
        }

        if (!this.options.minWidth) {
            return;
        }

        if (this.options.minWidth < 100 && this.options.resizable) {
            console.log("The minWidth when the resizable extension is active should be greater or equal than 100");
            this.options.minWidth = 100;
        }

        var that = this,
            old = {
                width: $(window).width(),
                height: $(window).height()
            };

        $(window).on('resize orientationchange',debounce(function (evt) {
            // reset view if height has only changed by at least the threshold.
            var height = $(this).height(),
                width = $(this).width();

            if (Math.abs(old.height - height) > that.options.heightThreshold || old.width != width) {
                changeView(that, width, height);
                old = {
                    width: width,
                    height: height
                };
            }
        },200));

        if (this.options.checkOnInit) {
            var height = $(window).height(),
                width = $(window).width();
            changeView(this, width, height);
            old = {
                width: width,
                height: height
            };
        }
    };
}(jQuery);
