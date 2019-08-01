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
 * Locale: TR (Turkish; Türkçe)
 */
$.extend( $.validator.messages, {
	required: "Bu alanın doldurulması zorunludur.",
	remote: "Lütfen bu alanı düzeltin.",
	email: "Lütfen geçerli bir e-posta adresi giriniz.",
	url: "Lütfen geçerli bir web adresi (URL) giriniz.",
	date: "Lütfen geçerli bir tarih giriniz.",
	dateISO: "Lütfen geçerli bir tarih giriniz(ISO formatında)",
	number: "Lütfen geçerli bir sayı giriniz.",
	digits: "Lütfen sadece sayısal karakterler giriniz.",
	creditcard: "Lütfen geçerli bir kredi kartı giriniz.",
	equalTo: "Lütfen aynı değeri tekrar giriniz.",
	extension: "Lütfen geçerli uzantıya sahip bir değer giriniz.",
	maxlength: $.validator.format( "Lütfen en fazla {0} karakter uzunluğunda bir değer giriniz." ),
	minlength: $.validator.format( "Lütfen en az {0} karakter uzunluğunda bir değer giriniz." ),
	rangelength: $.validator.format( "Lütfen en az {0} ve en fazla {1} uzunluğunda bir değer giriniz." ),
	range: $.validator.format( "Lütfen {0} ile {1} arasında bir değer giriniz." ),
	max: $.validator.format( "Lütfen {0} değerine eşit ya da daha küçük bir değer giriniz." ),
	min: $.validator.format( "Lütfen {0} değerine eşit ya da daha büyük bir değer giriniz." ),
	require_from_group: "Lütfen bu alanların en az {0} tanesini doldurunuz."
} );
return $;
}));