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
 * Bootstrap Table Vietnamese translation
 * Author: Duc N. PHAM <pngduc@gmail.com>
 */
(function ($) {
    'use strict';

    $.fn.bootstrapTable.locales['vi-VN'] = {
        formatLoadingMessage: function () {
            return 'Đang tải...';
        },
        formatRecordsPerPage: function (pageNumber) {
            return pageNumber + ' bản ghi mỗi trang';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return 'Hiển thị từ trang ' + pageFrom + ' đến ' + pageTo + ' của ' + totalRows + ' bảng ghi';
        },
        formatSearch: function () {
            return 'Tìm kiếm';
        },
        formatNoMatches: function () {
            return 'Không có dữ liệu';
        }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['vi-VN']);

})(jQuery);