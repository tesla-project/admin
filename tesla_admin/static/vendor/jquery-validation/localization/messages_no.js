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
 * Locale: NO (Norwegian; Norsk)
 */
$.extend( $.validator.messages, {
	required: "Dette feltet er obligatorisk.",
	maxlength: $.validator.format( "Maksimalt {0} tegn." ),
	minlength: $.validator.format( "Minimum {0} tegn." ),
	rangelength: $.validator.format( "Angi minimum {0} og maksimum {1} tegn." ),
	email: "Oppgi en gyldig epostadresse.",
	url: "Angi en gyldig URL.",
	date: "Angi en gyldig dato.",
	dateISO: "Angi en gyldig dato (&ARING;&ARING;&ARING;&ARING;-MM-DD).",
	dateSE: "Angi en gyldig dato.",
	number: "Angi et gyldig nummer.",
	numberSE: "Angi et gyldig nummer.",
	digits: "Skriv kun tall.",
	equalTo: "Skriv samme verdi igjen.",
	range: $.validator.format( "Angi en verdi mellom {0} og {1}." ),
	max: $.validator.format( "Angi en verdi som er mindre eller lik {0}." ),
	min: $.validator.format( "Angi en verdi som er st&oslash;rre eller lik {0}." ),
	step: $.validator.format( "Angi en verdi ganger {0}." ),
	creditcard: "Angi et gyldig kredittkortnummer."
} );
return $;
}));