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

(function( factory ) {
	if ( typeof define === "function" && define.amd ) {
		define( ["jquery", "../jquery.validate"], factory );
	} else if (typeof module === "object" && module.exports) {
		module.exports = factory( require( "jquery" ) );
	} else {
		factory( jQuery );
	}
}(function( $ ) {

/*
 * Translated default messages for the jQuery validation plugin.
 * Locale: ZH (Chinese; 中文 (Zhōngwén), 汉语, 漢語)
 * Region: TW (Taiwan)
 */
$.extend( $.validator.messages, {
	required: "必須填寫",
	remote: "請修正此欄位",
	email: "請輸入有效的電子郵件",
	url: "請輸入有效的網址",
	date: "請輸入有效的日期",
	dateISO: "請輸入有效的日期 (YYYY-MM-DD)",
	number: "請輸入正確的數值",
	digits: "只可輸入數字",
	creditcard: "請輸入有效的信用卡號碼",
	equalTo: "請重複輸入一次",
	extension: "請輸入有效的後綴",
	maxlength: $.validator.format( "最多 {0} 個字" ),
	minlength: $.validator.format( "最少 {0} 個字" ),
	rangelength: $.validator.format( "請輸入長度為 {0} 至 {1} 之間的字串" ),
	range: $.validator.format( "請輸入 {0} 至 {1} 之間的數值" ),
	max: $.validator.format( "請輸入不大於 {0} 的數值" ),
	min: $.validator.format( "請輸入不小於 {0} 的數值" )
} );
return $;
}));