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
 * Locale: RO (Romanian, limba română)
 */
$.extend( $.validator.messages, {
	required: "Acest câmp este obligatoriu.",
	remote: "Te rugăm să completezi acest câmp.",
	email: "Te rugăm să introduci o adresă de email validă",
	url: "Te rugăm sa introduci o adresă URL validă.",
	date: "Te rugăm să introduci o dată corectă.",
	dateISO: "Te rugăm să introduci o dată (ISO) corectă.",
	number: "Te rugăm să introduci un număr întreg valid.",
	digits: "Te rugăm să introduci doar cifre.",
	creditcard: "Te rugăm să introduci un numar de carte de credit valid.",
	equalTo: "Te rugăm să reintroduci valoarea.",
	extension: "Te rugăm să introduci o valoare cu o extensie validă.",
	maxlength: $.validator.format( "Te rugăm să nu introduci mai mult de {0} caractere." ),
	minlength: $.validator.format( "Te rugăm să introduci cel puțin {0} caractere." ),
	rangelength: $.validator.format( "Te rugăm să introduci o valoare între {0} și {1} caractere." ),
	range: $.validator.format( "Te rugăm să introduci o valoare între {0} și {1}." ),
	max: $.validator.format( "Te rugăm să introduci o valoare egal sau mai mică decât {0}." ),
	min: $.validator.format( "Te rugăm să introduci o valoare egal sau mai mare decât {0}." )
} );
return $;
}));