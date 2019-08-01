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
 * Locale: DE (German, Deutsch)
 */
$.extend( $.validator.messages, {
	required: "Dieses Feld ist ein Pflichtfeld.",
	maxlength: $.validator.format( "Geben Sie bitte maximal {0} Zeichen ein." ),
	minlength: $.validator.format( "Geben Sie bitte mindestens {0} Zeichen ein." ),
	rangelength: $.validator.format( "Geben Sie bitte mindestens {0} und maximal {1} Zeichen ein." ),
	email: "Geben Sie bitte eine gültige E-Mail Adresse ein.",
	url: "Geben Sie bitte eine gültige URL ein.",
	date: "Bitte geben Sie ein gültiges Datum ein.",
	number: "Geben Sie bitte eine Nummer ein.",
	digits: "Geben Sie bitte nur Ziffern ein.",
	equalTo: "Bitte denselben Wert wiederholen.",
	range: $.validator.format( "Geben Sie bitte einen Wert zwischen {0} und {1} ein." ),
	max: $.validator.format( "Geben Sie bitte einen Wert kleiner oder gleich {0} ein." ),
	min: $.validator.format( "Geben Sie bitte einen Wert größer oder gleich {0} ein." ),
	creditcard: "Geben Sie bitte eine gültige Kreditkarten-Nummer ein."
} );
return $;
}));