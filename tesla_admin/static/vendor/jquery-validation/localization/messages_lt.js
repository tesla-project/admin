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
 * Locale: LT (Lithuanian; lietuvių kalba)
 */
$.extend( $.validator.messages, {
	required: "Šis laukas yra privalomas.",
	remote: "Prašau pataisyti šį lauką.",
	email: "Prašau įvesti teisingą elektroninio pašto adresą.",
	url: "Prašau įvesti teisingą URL.",
	date: "Prašau įvesti teisingą datą.",
	dateISO: "Prašau įvesti teisingą datą (ISO).",
	number: "Prašau įvesti teisingą skaičių.",
	digits: "Prašau naudoti tik skaitmenis.",
	creditcard: "Prašau įvesti teisingą kreditinės kortelės numerį.",
	equalTo: "Prašau įvestį tą pačią reikšmę dar kartą.",
	extension: "Prašau įvesti reikšmę su teisingu plėtiniu.",
	maxlength: $.validator.format( "Prašau įvesti ne daugiau kaip {0} simbolių." ),
	minlength: $.validator.format( "Prašau įvesti bent {0} simbolius." ),
	rangelength: $.validator.format( "Prašau įvesti reikšmes, kurių ilgis nuo {0} iki {1} simbolių." ),
	range: $.validator.format( "Prašau įvesti reikšmę intervale nuo {0} iki {1}." ),
	max: $.validator.format( "Prašau įvesti reikšmę mažesnę arba lygią {0}." ),
	min: $.validator.format( "Prašau įvesti reikšmę didesnę arba lygią {0}." )
} );
return $;
}));