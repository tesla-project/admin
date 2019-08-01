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
 * Locale: BG (Bulgarian; български език)
 */
$.extend( $.validator.messages, {
	required: "Полето е задължително.",
	remote: "Моля, въведете правилната стойност.",
	email: "Моля, въведете валиден email.",
	url: "Моля, въведете валидно URL.",
	date: "Моля, въведете валидна дата.",
	dateISO: "Моля, въведете валидна дата (ISO).",
	number: "Моля, въведете валиден номер.",
	digits: "Моля, въведете само цифри.",
	creditcard: "Моля, въведете валиден номер на кредитна карта.",
	equalTo: "Моля, въведете същата стойност отново.",
	extension: "Моля, въведете стойност с валидно разширение.",
	maxlength: $.validator.format( "Моля, въведете повече от {0} символа." ),
	minlength: $.validator.format( "Моля, въведете поне {0} символа." ),
	rangelength: $.validator.format( "Моля, въведете стойност с дължина между {0} и {1} символа." ),
	range: $.validator.format( "Моля, въведете стойност между {0} и {1}." ),
	max: $.validator.format( "Моля, въведете стойност по-малка или равна на {0}." ),
	min: $.validator.format( "Моля, въведете стойност по-голяма или равна на {0}." )
} );
return $;
}));