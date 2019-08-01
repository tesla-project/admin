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

/**
 * @author  @tatocaster <kutaliatato@gmail.com>
 * Translated default messages for the jQuery validation plugin.
 * Locale: GE (Georgian; ქართული)
 */
$.extend( $.validator.messages, {
	required: "ეს ველი სავალდებულოა",
	remote: "გთხოვთ შეასწოროთ.",
	email: "გთხოვთ შეიყვანოთ სწორი ფორმატით.",
	url: "გთხოვთ შეიყვანოთ სწორი ფორმატით.",
	date: "გთხოვთ შეიყვანოთ სწორი თარიღი.",
	dateISO: "გთხოვთ შეიყვანოთ სწორი ფორმატით (ISO).",
	number: "გთხოვთ შეიყვანოთ რიცხვი.",
	digits: "დაშვებულია მხოლოდ ციფრები.",
	creditcard: "გთხოვთ შეიყვანოთ სწორი ფორმატის ბარათის კოდი.",
	equalTo: "გთხოვთ შეიყვანოთ იგივე მნიშვნელობა.",
	maxlength: $.validator.format( "გთხოვთ შეიყვანოთ არა უმეტეს {0} სიმბოლოსი." ),
	minlength: $.validator.format( "შეიყვანეთ მინიმუმ {0} სიმბოლო." ),
	rangelength: $.validator.format( "გთხოვთ შეიყვანოთ {0} -დან {1} -მდე რაოდენობის სიმბოლოები." ),
	range: $.validator.format( "შეიყვანეთ {0} -სა {1} -ს შორის." ),
	max: $.validator.format( "გთხოვთ შეიყვანოთ მნიშვნელობა ნაკლები ან ტოლი {0} -ს." ),
	min: $.validator.format( "გთხოვთ შეიყვანოთ მნიშვნელობა მეტი ან ტოლი {0} -ს." )
} );
return $;
}));