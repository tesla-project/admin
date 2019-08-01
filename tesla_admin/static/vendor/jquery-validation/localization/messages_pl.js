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
 * Locale: PL (Polish; język polski, polszczyzna)
 */
$.extend( $.validator.messages, {
	required: "To pole jest wymagane.",
	remote: "Proszę o wypełnienie tego pola.",
	email: "Proszę o podanie prawidłowego adresu email.",
	url: "Proszę o podanie prawidłowego URL.",
	date: "Proszę o podanie prawidłowej daty.",
	dateISO: "Proszę o podanie prawidłowej daty (ISO).",
	number: "Proszę o podanie prawidłowej liczby.",
	digits: "Proszę o podanie samych cyfr.",
	creditcard: "Proszę o podanie prawidłowej karty kredytowej.",
	equalTo: "Proszę o podanie tej samej wartości ponownie.",
	extension: "Proszę o podanie wartości z prawidłowym rozszerzeniem.",
	nipPL: "Proszę o podanie prawidłowego numeru NIP.",
	maxlength: $.validator.format( "Proszę o podanie nie więcej niż {0} znaków." ),
	minlength: $.validator.format( "Proszę o podanie przynajmniej {0} znaków." ),
	rangelength: $.validator.format( "Proszę o podanie wartości o długości od {0} do {1} znaków." ),
	range: $.validator.format( "Proszę o podanie wartości z przedziału od {0} do {1}." ),
	max: $.validator.format( "Proszę o podanie wartości mniejszej bądź równej {0}." ),
	min: $.validator.format( "Proszę o podanie wartości większej bądź równej {0}." ),
	pattern: $.validator.format( "Pole zawiera niedozwolone znaki." )
} );
return $;
}));