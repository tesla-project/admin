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
 * Locale: KA (Georgian; ქართული)
 */
$.extend( $.validator.messages, {
	required: "ამ ველის შევსება აუცილებელია.",
	remote: "გთხოვთ მიუთითოთ სწორი მნიშვნელობა.",
	email: "გთხოვთ მიუთითოთ ელ-ფოსტის კორექტული მისამართი.",
	url: "გთხოვთ მიუთითოთ კორექტული URL.",
	date: "გთხოვთ მიუთითოთ კორექტული თარიღი.",
	dateISO: "გთხოვთ მიუთითოთ კორექტული თარიღი ISO ფორმატში.",
	number: "გთხოვთ მიუთითოთ ციფრი.",
	digits: "გთხოვთ მიუთითოთ მხოლოდ ციფრები.",
	creditcard: "გთხოვთ მიუთითოთ საკრედიტო ბარათის კორექტული ნომერი.",
	equalTo: "გთხოვთ მიუთითოთ ასეთივე მნიშვნელობა კიდევ ერთხელ.",
	extension: "გთხოვთ აირჩიოთ ფაილი კორექტული გაფართოებით.",
	maxlength: $.validator.format( "დასაშვებია არაუმეტეს {0} სიმბოლო." ),
	minlength: $.validator.format( "აუცილებელია შეიყვანოთ მინიმუმ {0} სიმბოლო." ),
	rangelength: $.validator.format( "ტექსტში სიმბოლოების რაოდენობა უნდა იყოს {0}-დან {1}-მდე." ),
	range: $.validator.format( "გთხოვთ შეიყვანოთ ციფრი {0}-დან {1}-მდე." ),
	max: $.validator.format( "გთხოვთ შეიყვანოთ ციფრი რომელიც ნაკლებია ან უდრის {0}-ს." ),
	min: $.validator.format( "გთხოვთ შეიყვანოთ ციფრი რომელიც მეტია ან უდრის {0}-ს." )
} );
return $;
}));