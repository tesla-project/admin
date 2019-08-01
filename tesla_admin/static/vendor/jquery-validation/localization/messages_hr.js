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
 * Locale: HR (Croatia; hrvatski jezik)
 */
$.extend( $.validator.messages, {
	required: "Ovo polje je obavezno.",
	remote: "Ovo polje treba popraviti.",
	email: "Unesite ispravnu e-mail adresu.",
	url: "Unesite ispravan URL.",
	date: "Unesite ispravan datum.",
	dateISO: "Unesite ispravan datum (ISO).",
	number: "Unesite ispravan broj.",
	digits: "Unesite samo brojeve.",
	creditcard: "Unesite ispravan broj kreditne kartice.",
	equalTo: "Unesite ponovo istu vrijednost.",
	extension: "Unesite vrijednost sa ispravnom ekstenzijom.",
	maxlength: $.validator.format( "Maksimalni broj znakova je {0} ." ),
	minlength: $.validator.format( "Minimalni broj znakova je {0} ." ),
	rangelength: $.validator.format( "Unesite vrijednost između {0} i {1} znakova." ),
	range: $.validator.format( "Unesite vrijednost između {0} i {1}." ),
	max: $.validator.format( "Unesite vrijednost manju ili jednaku {0}." ),
	min: $.validator.format( "Unesite vrijednost veću ili jednaku {0}." )
} );
return $;
}));