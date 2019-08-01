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
 * Locale: AR (Arabic; العربية)
 */
$.extend( $.validator.messages, {
	required: "هذا الحقل إلزامي",
	remote: "يرجى تصحيح هذا الحقل للمتابعة",
	email: "رجاء إدخال عنوان بريد إلكتروني صحيح",
	url: "رجاء إدخال عنوان موقع إلكتروني صحيح",
	date: "رجاء إدخال تاريخ صحيح",
	dateISO: "رجاء إدخال تاريخ صحيح (ISO)",
	number: "رجاء إدخال عدد بطريقة صحيحة",
	digits: "رجاء إدخال أرقام فقط",
	creditcard: "رجاء إدخال رقم بطاقة ائتمان صحيح",
	equalTo: "رجاء إدخال نفس القيمة",
	extension: "رجاء إدخال ملف بامتداد موافق عليه",
	maxlength: $.validator.format( "الحد الأقصى لعدد الحروف هو {0}" ),
	minlength: $.validator.format( "الحد الأدنى لعدد الحروف هو {0}" ),
	rangelength: $.validator.format( "عدد الحروف يجب أن يكون بين {0} و {1}" ),
	range: $.validator.format( "رجاء إدخال عدد قيمته بين {0} و {1}" ),
	max: $.validator.format( "رجاء إدخال عدد أقل من أو يساوي {0}" ),
	min: $.validator.format( "رجاء إدخال عدد أكبر من أو يساوي {0}" )
} );
return $;
}));