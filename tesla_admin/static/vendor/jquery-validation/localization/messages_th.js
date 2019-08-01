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
 * Locale: TH (Thai; ไทย)
 */
$.extend( $.validator.messages, {
	required: "โปรดระบุ",
	remote: "โปรดแก้ไขให้ถูกต้อง",
	email: "โปรดระบุที่อยู่อีเมล์ที่ถูกต้อง",
	url: "โปรดระบุ URL ที่ถูกต้อง",
	date: "โปรดระบุวันที่ ที่ถูกต้อง",
	dateISO: "โปรดระบุวันที่ ที่ถูกต้อง (ระบบ ISO).",
	number: "โปรดระบุทศนิยมที่ถูกต้อง",
	digits: "โปรดระบุจำนวนเต็มที่ถูกต้อง",
	creditcard: "โปรดระบุรหัสบัตรเครดิตที่ถูกต้อง",
	equalTo: "โปรดระบุค่าเดิมอีกครั้ง",
	extension: "โปรดระบุค่าที่มีส่วนขยายที่ถูกต้อง",
	maxlength: $.validator.format( "โปรดอย่าระบุค่าที่ยาวกว่า {0} อักขระ" ),
	minlength: $.validator.format( "โปรดอย่าระบุค่าที่สั้นกว่า {0} อักขระ" ),
	rangelength: $.validator.format( "โปรดอย่าระบุค่าความยาวระหว่าง {0} ถึง {1} อักขระ" ),
	range: $.validator.format( "โปรดระบุค่าระหว่าง {0} และ {1}" ),
	max: $.validator.format( "โปรดระบุค่าน้อยกว่าหรือเท่ากับ {0}" ),
	min: $.validator.format( "โปรดระบุค่ามากกว่าหรือเท่ากับ {0}" )
} );
return $;
}));