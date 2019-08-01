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
 * Bootstrap Table Japanese translation
 * Author: Azamshul Azizy <azamshul@gmail.com>
 */
(function ($) {
    'use strict';

    $.fn.bootstrapTable.locales['ja-JP'] = {
        formatLoadingMessage: function () {
            return '読み込み中です。少々お待ちください。';
        },
        formatRecordsPerPage: function (pageNumber) {
            return 'ページ当たり最大' + pageNumber + '件';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return '全' + totalRows + '件から、'+ pageFrom + 'から' + pageTo + '件目まで表示しています';
        },
        formatSearch: function () {
            return '検索';
        },
        formatNoMatches: function () {
            return '該当するレコードが見つかりません';
        },
        formatPaginationSwitch: function () {
            return 'ページ数を表示・非表示';
        },
        formatRefresh: function () {
            return '更新';
        },
        formatToggle: function () {
            return 'トグル';
        },
        formatColumns: function () {
            return '列';
        },
        formatAllRows: function () {
            return 'すべて';
        }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['ja-JP']);

})(jQuery);