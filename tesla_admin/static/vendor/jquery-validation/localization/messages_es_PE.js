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
 * Locale: ES (Spanish; Español)
 * Region: PE (Perú)
 */
$.extend( $.validator.messages, {
	required: "Este campo es obligatorio.",
	remote: "Por favor, llene este campo.",
	email: "Por favor, escriba un correo electrónico válido.",
	url: "Por favor, escriba una URL válida.",
	date: "Por favor, escriba una fecha válida.",
	dateISO: "Por favor, escriba una fecha (ISO) válida.",
	number: "Por favor, escriba un número válido.",
	digits: "Por favor, escriba sólo dígitos.",
	creditcard: "Por favor, escriba un número de tarjeta válido.",
	equalTo: "Por favor, escriba el mismo valor de nuevo.",
	extension: "Por favor, escriba un valor con una extensión permitida.",
	maxlength: $.validator.format( "Por favor, no escriba más de {0} caracteres." ),
	minlength: $.validator.format( "Por favor, no escriba menos de {0} caracteres." ),
	rangelength: $.validator.format( "Por favor, escriba un valor entre {0} y {1} caracteres." ),
	range: $.validator.format( "Por favor, escriba un valor entre {0} y {1}." ),
	max: $.validator.format( "Por favor, escriba un valor menor o igual a {0}." ),
	min: $.validator.format( "Por favor, escriba un valor mayor o igual a {0}." ),
	nifES: "Por favor, escriba un NIF válido.",
	nieES: "Por favor, escriba un NIE válido.",
	cifES: "Por favor, escriba un CIF válido."
} );
return $;
}));