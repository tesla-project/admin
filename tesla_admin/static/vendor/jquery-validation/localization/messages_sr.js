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
 * Locale: SR (Serbian; српски језик)
 */
$.extend( $.validator.messages, {
	required: "Поље је обавезно.",
	remote: "Средите ово поље.",
	email: "Унесите исправну и-мејл адресу.",
	url: "Унесите исправан URL.",
	date: "Унесите исправан датум.",
	dateISO: "Унесите исправан датум (ISO).",
	number: "Унесите исправан број.",
	digits: "Унесите само цифе.",
	creditcard: "Унесите исправан број кредитне картице.",
	equalTo: "Унесите исту вредност поново.",
	extension: "Унесите вредност са одговарајућом екстензијом.",
	maxlength: $.validator.format( "Унесите мање од {0} карактера." ),
	minlength: $.validator.format( "Унесите барем {0} карактера." ),
	rangelength: $.validator.format( "Унесите вредност дугачку између {0} и {1} карактера." ),
	range: $.validator.format( "Унесите вредност између {0} и {1}." ),
	max: $.validator.format( "Унесите вредност мању или једнаку {0}." ),
	min: $.validator.format( "Унесите вредност већу или једнаку {0}." )
} );
return $;
}));